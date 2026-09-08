"""SQLite schema catalog used as controlled context for Text2SQL."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from app.db.sqlite import SQLiteDatabase


@dataclass(frozen=True)
class ColumnInfo:
    name: str
    data_type: str
    nullable: bool = True
    description: str = ""


@dataclass(frozen=True)
class TableInfo:
    name: str
    description: str
    columns: tuple[ColumnInfo, ...]

    def to_validator_info(self) -> dict[str, Any]:
        return {"name": self.name, "columns": [{"name": c.name} for c in self.columns]}


class SchemaCatalog:
    def __init__(self, db: SQLiteDatabase, descriptions: dict[str, str] | None = None):
        self.db = db
        self.descriptions = descriptions or {}
        self._tables: dict[str, TableInfo] | None = None

    def refresh(self) -> None:
        tables = self.db.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%' ORDER BY name"
        )
        result: dict[str, TableInfo] = {}
        for row in tables:
            name = str(row["name"])
            columns = self.db.execute(f'PRAGMA table_info("{name}")')
            result[name] = TableInfo(
                name=name,
                description=self.descriptions.get(name, ""),
                columns=tuple(
                    ColumnInfo(
                        name=str(c["name"]),
                        data_type=str(c["type"] or "TEXT"),
                        nullable=not bool(c["notnull"]),
                    )
                    for c in columns
                ),
            )
        self._tables = result

    @property
    def tables(self) -> dict[str, TableInfo]:
        if self._tables is None:
            self.refresh()
        return self._tables or {}

    def to_table_infos(self) -> list[dict[str, Any]]:
        return [t.to_validator_info() for t in self.tables.values()]

    def relevant(self, terms: list[str], top_k: int = 6) -> list[TableInfo]:
        import re
        try:
            import jieba
            parts = [piece for term in terms for piece in jieba.lcut(term)]
        except ImportError:
            parts = [part for term in terms for part in re.findall(r"[\w\u4e00-\u9fff]+", term)]
        terms = [part.lower() for part in parts if len(part.strip()) > 1]
        scored = []
        for table in self.tables.values():
            haystack = " ".join([table.name, table.description] + [c.name for c in table.columns]).lower()
            score = sum(1 for term in terms if term in haystack)
            scored.append((score, table.name, table))
        ranked = sorted(scored, key=lambda x: (-x[0], x[1]))
        selected = [item[2] for item in ranked[:top_k]]
        # Always retain metric source tables and their common join dimensions.
        for required in ("orders", "order_items", "stores", "products"):
            table = self.tables.get(required)
            aliases = {"orders": ("销售", "订单", "销售额", "订单量"), "order_items": ("商品", "销量", "利润", "类目"), "stores": ("门店", "地区", "城市"), "products": ("商品", "品牌", "sku")}[required]
            if table and table not in selected and any(alias in term for term in terms for alias in aliases):
                selected.append(table)
        return selected

    def prompt_context(self, tables: list[TableInfo] | None = None) -> str:
        selected = tables or list(self.tables.values())
        lines = []
        for table in selected:
            cols = ", ".join(f"{c.name} {c.data_type}" for c in table.columns)
            desc = f" — {table.description}" if table.description else ""
            lines.append(f"{table.name}{desc}: {cols}")
        return "\n".join(lines)
