"""
企业经营数据分析 Agent - 模拟数据生成器
==========================================

规模：中等业务数据集 (B)
- 20 门店
- 10 商品类目
- 5000 SKU
- 20000 客户
- 50000 订单
- ~150000 订单明细
- 5000 退款
- 10000 库存变动

时间跨度：2024-01-01 ~ 2026-09-30（约 33 个月）

支持：MySQL 8.0（生产）/ SQLite（本地演示）

用法：
    # 生成 SQLite 演示数据
    python generate_data.py --db sqlite --output enterprise.db

    # 生成 MySQL 数据（写入真实数据库）
    python generate_data.py --db mysql --dsn "mysql+pymysql://user:pass@host:3306/db"
"""

import argparse
import random
import sys
from datetime import datetime, timedelta, date
from pathlib import Path

import pandas as pd
from faker import Faker
from sqlalchemy import create_engine, text
from tqdm import tqdm

# ============================================================
# 配置常量
# ============================================================
SEED = 42
random.seed(SEED)

START_DATE = datetime(2024, 1, 1)
END_DATE = datetime(2026, 9, 30, 23, 59, 59)
DAYS_TOTAL = (END_DATE - START_DATE).days

N_STORES = 20
N_CATEGORIES = 10
N_PRODUCTS = 5000
N_CUSTOMERS = 20000
N_ORDERS = 50000
N_INVENTORY_LOGS = 10000

# 业务参数
BRANDS = ["Apple", "华为", "小米", "OPPO", "vivo", "三星", "其他"]
BRAND_WEIGHTS = [0.30, 0.25, 0.18, 0.10, 0.08, 0.06, 0.03]  # Apple 最高
CHANNELS = ["app", "miniprogram", "web", "offline"]
CHANNEL_WEIGHTS = [0.45, 0.30, 0.15, 0.10]
PAYMENT_METHODS = ["wechat", "alipay", "card", "installment"]
PAYMENT_WEIGHTS = [0.45, 0.40, 0.10, 0.05]
ORDER_STATUSES = ["created", "paid", "shipped", "completed", "cancelled"]
REFUND_REASONS = ["质量问题", "不想要了", "物流问题", "描述不符", "其他"]
REFUND_TYPES = ["仅退款", "退货退款", "换货"]
REGIONS = ["华中", "华东", "华南", "华北", "西南", "西北", "东北"]
CITIES = {
    "华中": ["长沙", "武汉", "郑州", "南昌", "合肥"],
    "华东": ["上海", "南京", "苏州", "杭州", "宁波"],
    "华南": ["广州", "深圳", "东莞", "佛山", "厦门"],
    "华北": ["北京", "天津", "石家庄", "太原", "济南"],
    "西南": ["成都", "重庆", "昆明", "贵阳", "拉萨"],
    "西北": ["西安", "兰州", "西宁", "银川", "乌鲁木齐"],
    "东北": ["沈阳", "大连", "哈尔滨", "长春", "齐齐哈尔"],
}
CUSTOMER_LEVELS = ["普通", "银卡", "金卡", "铂金"]
CUSTOMER_LEVEL_WEIGHTS = [0.60, 0.25, 0.12, 0.03]
STORE_TYPES = ["直营", "加盟", "体验店"]
STORE_TYPE_WEIGHTS = [0.50, 0.35, 0.15]

CATEGORY_NAMES = [
    "智能手机", "配件", "智能穿戴", "耳机音箱", "平板电脑",
    "笔记本电脑", "智能家居", "摄影摄像", "游戏设备", "办公设备",
]

PRODUCT_PREFIXES = {
    "智能手机": ["Pro", "Plus", "Max", "Ultra", "标准版", "青春版"],
    "耳机音箱": ["Pro", "Lite", "Studio", "Air", "Buds", "Sound"],
    "智能穿戴": ["Watch", "Band", "Fit", "Sport", "Pro"],
    "笔记本电脑": ["Air", "Pro", "Book", "Plus", "X"],
}

# ============================================================
# 工具函数
# ============================================================
fake = Faker("zh_CN")
Faker.seed(SEED)


def random_datetime(start: datetime, end: datetime) -> datetime:
    delta = end - start
    seconds = random.randint(0, int(delta.total_seconds()))
    return start + timedelta(seconds=seconds)


def weighted_choice(items, weights):
    return random.choices(items, weights=weights, k=1)[0]


def is_double_eleven(dt: datetime) -> bool:
    """双 11 大促因子"""
    if dt.month == 11 and 1 <= dt.day <= 11:
        return 1.8
    if dt.month == 11 and 12 <= dt.day <= 18:
        return 1.3
    # 618 年中大促
    if dt.month == 6 and 1 <= dt.day <= 18:
        return 1.4
    # 春节淡季
    if dt.month == 2:
        return 0.6
    return 1.0


def is_weekend(dt: datetime) -> bool:
    return dt.weekday() >= 5


# ============================================================
# 1. 门店
# ============================================================
def gen_stores() -> pd.DataFrame:
    rows = []
    for i in range(1, N_STORES + 1):
        region = random.choice(REGIONS)
        city = random.choice(CITIES[region])
        store_type = weighted_choice(STORE_TYPES, STORE_TYPE_WEIGHTS)
        store_name = f"{city}{['五一广场', '万达', '万象城', 'IFS', '解放路', '中山路', '步行街', '新天地'][i % 8]}{['旗舰店', '体验店', '授权店', '专卖店'][i % 4]}"
        opened_at = START_DATE.date() - timedelta(days=random.randint(30, 1500))
        rows.append({
            "store_id": i,
            "store_name": store_name,
            "city": city,
            "region": region,
            "store_type": store_type,
            "opened_at": opened_at,
            "is_active": 1 if random.random() > 0.05 else 0,
        })
    return pd.DataFrame(rows)


# ============================================================
# 2. 类目
# ============================================================
def gen_categories() -> pd.DataFrame:
    rows = []
    for i, name in enumerate(CATEGORY_NAMES, start=1):
        rows.append({
            "category_id": i,
            "category_name": name,
            "parent_id": None,
            "level": 1,
            "sort_order": i,
        })
    return pd.DataFrame(rows)


# ============================================================
# 3. 商品
# ============================================================
def gen_products() -> pd.DataFrame:
    rows = []
    for i in range(1, N_PRODUCTS + 1):
        brand = weighted_choice(BRANDS, BRAND_WEIGHTS)
        category_id = random.randint(1, N_CATEGORIES)
        category_name = CATEGORY_NAMES[category_id - 1]
        prefix_options = PRODUCT_PREFIXES.get(category_name, ["标准版", "Pro", "Plus"])
        prefix = random.choice(prefix_options)

        # 价格区间：智能手机贵，配件便宜
        if category_name == "智能手机":
            cost = round(random.uniform(2000, 8000), 2)
            sale = round(cost * random.uniform(1.10, 1.30), 2)
        elif category_name in ["笔记本电脑", "平板电脑", "摄影摄像"]:
            cost = round(random.uniform(800, 5000), 2)
            sale = round(cost * random.uniform(1.15, 1.35), 2)
        else:
            cost = round(random.uniform(20, 500), 2)
            sale = round(cost * random.uniform(1.20, 1.50), 2)

        sku_code = f"{brand[:2].upper()}-{category_id:02d}-{i:05d}"
        product_name = f"{brand} {category_name} {prefix} {random.choice(['黑色', '白色', '蓝色', '银色', '金色', '绿色'])}"
        created_at = random_datetime(START_DATE, datetime(2025, 6, 30))

        rows.append({
            "product_id": i,
            "sku_code": sku_code,
            "product_name": product_name,
            "brand": brand,
            "category_id": category_id,
            "cost_price": cost,
            "sale_price": sale,
            "is_active": 1 if random.random() > 0.10 else 0,
            "created_at": created_at,
        })
    return pd.DataFrame(rows)


# ============================================================
# 4. 客户
# ============================================================
def gen_customers() -> pd.DataFrame:
    rows = []
    for i in range(1, N_CUSTOMERS + 1):
        region = random.choice(REGIONS)
        city = random.choice(CITIES[region])
        gender = random.choice(["M", "F"])
        age = random.randint(18, 70)
        level = weighted_choice(CUSTOMER_LEVELS, CUSTOMER_LEVEL_WEIGHTS)
        registered_at = random_datetime(START_DATE, END_DATE)
        rows.append({
            "customer_id": i,
            "customer_name": fake.name_male() if gender == "M" else fake.name_female(),
            "gender": gender,
            "age": age,
            "city": city,
            "customer_level": level,
            "registered_at": registered_at,
            "is_active": 1,
        })
    return pd.DataFrame(rows)


# ============================================================
# 5. 订单（含订单明细、支付）
# ============================================================
def gen_orders_and_items(products_df: pd.DataFrame, customers_df: pd.DataFrame,
                          stores_df: pd.DataFrame) -> tuple:
    """生成订单 + 订单明细 + 支付记录"""
    orders = []
    items = []
    payments = []

    product_ids = products_df["product_id"].tolist()
    customer_ids = customers_df["customer_id"].tolist()
    store_ids = stores_df["store_id"].tolist()

    # 商品价格表（避免每条都查）
    price_map = products_df.set_index("product_id")[["sale_price", "brand", "product_name", "sku_code"]].to_dict("index")

    item_id_counter = 1
    payment_id_counter = 1

    for i in tqdm(range(1, N_ORDERS + 1), desc="生成订单"):
        # 决定订单时间：周末 + 大促因子加权
        base_dt = random_datetime(START_DATE, END_DATE)
        while random.random() > is_double_eleven(base_dt) * (1.3 if is_weekend(base_dt) else 1.0):
            base_dt = random_datetime(START_DATE, END_DATE)

        # 决定订单状态（按时间衰减：旧订单大概率已完成，新订单可能待支付）
        age_days = (END_DATE - base_dt).days
        if age_days > 60:
            status = weighted_choice(["completed", "cancelled", "refunded"], [0.85, 0.10, 0.05])
        elif age_days > 7:
            status = weighted_choice(["completed", "shipped", "cancelled", "paid"], [0.70, 0.15, 0.08, 0.07])
        else:
            status = weighted_choice(["paid", "shipped", "created", "cancelled"], [0.50, 0.30, 0.15, 0.05])

        customer_id = random.choice(customer_ids)
        store_id = random.choice(store_ids)
        channel = weighted_choice(CHANNELS, CHANNEL_WEIGHTS)

        # 订单项数（1-5 件）
        n_items = random.choices([1, 2, 3, 4, 5], weights=[0.40, 0.30, 0.18, 0.08, 0.04])[0]
        item_records = random.sample(product_ids, n_items)

        subtotal = 0.0
        for prod_id in item_records:
            qty = random.choices([1, 2, 3], weights=[0.70, 0.20, 0.10])[0]
            unit_price = price_map[prod_id]["sale_price"] * random.uniform(0.90, 1.00)  # 略有议价
            line_subtotal = round(qty * unit_price, 2)
            subtotal += line_subtotal

            items.append({
                "item_id": item_id_counter,
                "order_id": i,
                "product_id": prod_id,
                "sku_code": price_map[prod_id]["sku_code"],
                "product_name": price_map[prod_id]["product_name"],
                "brand": price_map[prod_id]["brand"],
                "quantity": qty,
                "unit_price": unit_price,
                "subtotal_amount": line_subtotal,
            })
            item_id_counter += 1

        discount = round(subtotal * random.uniform(0, 0.15), 2) if random.random() < 0.3 else 0
        freight = 0 if subtotal > 99 else 10
        paid = round(subtotal - discount + freight, 2)

        # 时间状态机
        created = base_dt
        paid_at = created + timedelta(minutes=random.randint(1, 30)) if status != "created" else None
        shipped_at = paid_at + timedelta(hours=random.randint(2, 48)) if status in ("shipped", "completed") else None
        completed_at = (shipped_at or paid_at) + timedelta(days=random.randint(1, 7)) if status == "completed" else None
        cancelled_at = created + timedelta(hours=random.randint(1, 24)) if status == "cancelled" else None

        orders.append({
            "order_id": i,
            "order_no": f"SO{created.strftime('%Y%m%d')}{i:08d}",
            "customer_id": customer_id,
            "store_id": store_id,
            "order_status": status,
            "order_amount": round(subtotal, 2),
            "discount_amount": discount,
            "freight_amount": freight,
            "paid_amount": paid if paid_at else 0,
            "item_count": n_items,
            "channel": channel,
            "created_at": created,
            "paid_at": paid_at,
            "shipped_at": shipped_at,
            "completed_at": completed_at,
            "cancelled_at": cancelled_at,
        })

        # 支付记录
        if paid_at:
            payments.append({
                "payment_id": payment_id_counter,
                "order_id": i,
                "payment_method": weighted_choice(PAYMENT_METHODS, PAYMENT_WEIGHTS),
                "payment_amount": paid,
                "paid_at": paid_at,
                "transaction_id": f"TX{uuid_hex()}",
            })
            payment_id_counter += 1

    return (pd.DataFrame(orders), pd.DataFrame(items), pd.DataFrame(payments))


def uuid_hex() -> str:
    import uuid
    return uuid.uuid4().hex[:24].upper()


# ============================================================
# 6. 退款
# ============================================================
def gen_refunds(orders_df: pd.DataFrame, payments_df: pd.DataFrame) -> pd.DataFrame:
    """从已完成/已发货的订单中抽取约 10% 生成退款"""
    refundable = orders_df[orders_df["order_status"].isin(["completed", "shipped"])]
    sample = refundable.sample(n=int(len(refundable) * 0.10), random_state=SEED)

    payment_map = payments_df.set_index("order_id")[["payment_id", "paid_at"]].to_dict("index")
    rows = []
    refund_id = 1

    for _, order in tqdm(sample.iterrows(), total=len(sample), desc="生成退款"):
        pay_info = payment_map.get(order["order_id"])
        if not pay_info:
            continue

        # 退款时间基于支付时间后 1-90 天
        days_after = random.choices(
            [random.randint(1, 7), random.randint(8, 30), random.randint(31, 90)],
            weights=[0.50, 0.35, 0.15]
        )[0]
        requested_at = pay_info["paid_at"] + timedelta(days=days_after)

        # 退款金额：部分退款 vs 全额
        if random.random() < 0.3:
            refund_amt = order["paid_amount"]
            refund_type = "退货退款"
        else:
            refund_amt = round(order["paid_amount"] * random.uniform(0.2, 0.5), 2)
            refund_type = random.choice(["仅退款", "换货"])

        status = weighted_choice(["completed", "approved", "requested", "rejected"],
                                  [0.70, 0.15, 0.10, 0.05])
        completed_at = requested_at + timedelta(days=random.randint(1, 5)) if status == "completed" else None

        rows.append({
            "refund_id": refund_id,
            "order_id": int(order["order_id"]),
            "payment_id": int(pay_info["payment_id"]),
            "refund_reason": random.choice(REFUND_REASONS),
            "refund_type": refund_type,
            "refund_amount": refund_amt,
            "refund_status": status,
            "requested_at": requested_at,
            "completed_at": completed_at,
        })
        refund_id += 1

    return pd.DataFrame(rows)


# ============================================================
# 7. 库存变动
# ============================================================
def gen_inventory_logs(products_df: pd.DataFrame, stores_df: pd.DataFrame) -> pd.DataFrame:
    product_ids = products_df["product_id"].tolist()
    store_ids = stores_df["store_id"].tolist()
    rows = []

    for i in tqdm(range(1, N_INVENTORY_LOGS + 1), desc="生成库存变动"):
        change_type = random.choices(
            ["inbound", "outbound", "adjustment", "return"],
            weights=[0.35, 0.45, 0.10, 0.10]
        )[0]

        if change_type == "inbound":
            qty = random.randint(50, 500)
            ref_no = f"PO{random.randint(20240001, 20260930)}"
        elif change_type == "outbound":
            qty = -random.randint(1, 20)
            ref_no = f"SO{random.randint(20240001, 20260930)}"
        elif change_type == "return":
            qty = random.randint(1, 5)
            ref_no = f"RE{random.randint(20240001, 20260930)}"
        else:
            qty = random.choice([random.randint(-50, -1), random.randint(1, 50)])
            ref_no = None

        stock_after = random.randint(0, 1000)
        rows.append({
            "log_id": i,
            "store_id": random.choice(store_ids),
            "product_id": random.choice(product_ids),
            "change_type": change_type,
            "change_qty": qty,
            "stock_after": stock_after,
            "reference_no": ref_no,
            "created_at": random_datetime(START_DATE, END_DATE),
        })

    return pd.DataFrame(rows)


# ============================================================
# 写入数据库
# ============================================================
def write_dataframe(engine, df: pd.DataFrame, table_name: str, if_exists: str = "append"):
    """写入 DataFrame 到数据库"""
    df.to_sql(table_name, engine, if_exists=if_exists, index=False, chunksize=2000)


def generate_for_sqlite(output_path: str):
    """生成 SQLite 演示数据"""
    engine = create_engine(f"sqlite:///{output_path}", echo=False)

    print("[1/7] 生成门店 ...")
    stores_df = gen_stores()
    write_dataframe(engine, stores_df, "stores", if_exists="replace")

    print("[2/7] 生成类目 ...")
    categories_df = gen_categories()
    write_dataframe(engine, categories_df, "categories", if_exists="replace")

    print("[3/7] 生成商品 ...")
    products_df = gen_products()
    write_dataframe(engine, products_df, "products", if_exists="replace")

    print("[4/7] 生成客户 ...")
    customers_df = gen_customers()
    write_dataframe(engine, customers_df, "customers", if_exists="replace")

    print("[5/7] 生成订单 + 明细 + 支付 ...")
    orders_df, items_df, payments_df = gen_orders_and_items(products_df, customers_df, stores_df)
    write_dataframe(engine, orders_df, "orders", if_exists="replace")
    write_dataframe(engine, items_df, "order_items", if_exists="replace")
    write_dataframe(engine, payments_df, "payments", if_exists="replace")

    print("[6/7] 生成退款 ...")
    refunds_df = gen_refunds(orders_df, payments_df)
    write_dataframe(engine, refunds_df, "refunds", if_exists="replace")

    print("[7/7] 生成库存变动 ...")
    inventory_df = gen_inventory_logs(products_df, stores_df)
    write_dataframe(engine, inventory_df, "inventory_logs", if_exists="replace")

    # 打印统计
    with engine.connect() as conn:
        print("\n=== 数据生成完成 ===")
        for table in ["stores", "categories", "products", "customers",
                      "orders", "order_items", "payments", "refunds", "inventory_logs"]:
            count = conn.execute(text(f"SELECT COUNT(*) FROM {table}")).scalar()
            print(f"  {table:18s} {count:>8,} 行")

    print(f"\nSQLite 数据库已保存：{output_path}")
    print(f"文件大小：{Path(output_path).stat().st_size / 1024 / 1024:.2f} MB")


def generate_for_mysql(dsn: str):
    """生成 MySQL 数据"""
    engine = create_engine(dsn, echo=False)

    # 先执行 schema
    init_sql_path = Path(__file__).parent / "init.sql"
    print(f"执行 schema: {init_sql_path}")
    with engine.connect() as conn:
        for stmt in init_sql_path.read_text(encoding="utf-8").split(";"):
            stmt = stmt.strip()
            if stmt and not stmt.startswith("--"):
                try:
                    conn.execute(text(stmt))
                    conn.commit()
                except Exception as e:
                    print(f"  跳过: {stmt[:50]}... ({e})")

    # 生成数据
    generate_for_sqlite_via_engine(engine)


def generate_for_sqlite_via_engine(engine):
    """复用 SQLite 流程但用已有 engine"""
    print("[1/7] 生成门店 ...")
    stores_df = gen_stores()
    write_dataframe(engine, stores_df, "stores", if_exists="append")

    print("[2/7] 生成类目 ...")
    categories_df = gen_categories()
    write_dataframe(engine, categories_df, "categories", if_exists="append")

    print("[3/7] 生成商品 ...")
    products_df = gen_products()
    write_dataframe(engine, products_df, "products", if_exists="append")

    print("[4/7] 生成客户 ...")
    customers_df = gen_customers()
    write_dataframe(engine, customers_df, "customers", if_exists="append")

    print("[5/7] 生成订单 + 明细 + 支付 ...")
    orders_df, items_df, payments_df = gen_orders_and_items(products_df, customers_df, stores_df)
    write_dataframe(engine, orders_df, "orders", if_exists="append")
    write_dataframe(engine, items_df, "order_items", if_exists="append")
    write_dataframe(engine, payments_df, "payments", if_exists="append")

    print("[6/7] 生成退款 ...")
    refunds_df = gen_refunds(orders_df, payments_df)
    write_dataframe(engine, refunds_df, "refunds", if_exists="append")

    print("[7/7] 生成库存变动 ...")
    inventory_df = gen_inventory_logs(products_df, stores_df)
    write_dataframe(engine, inventory_df, "inventory_logs", if_exists="append")

    print("\n=== 数据生成完成 ===")


# ============================================================
# 入口
# ============================================================
def main():
    parser = argparse.ArgumentParser(description="企业经营数据分析 Agent - 模拟数据生成器")
    parser.add_argument("--db", choices=["sqlite", "mysql"], default="sqlite")
    parser.add_argument("--output", default="enterprise.db", help="SQLite 输出路径")
    parser.add_argument("--dsn", help="MySQL DSN, 如 mysql+pymysql://user:pass@host:3306/db")
    parser.add_argument("--scale", choices=["small", "medium", "large"], default="medium",
                        help="数据规模（small/medium/large，对应 A/B/C）")
    args = parser.parse_args()

    if args.scale == "small":
        print("⚠️  small 模式仅作演示，建议使用 medium")
        return 1

    if args.db == "sqlite":
        output = args.output if Path(args.output).is_absolute() else str(Path(__file__).parent / args.output)
        generate_for_sqlite(output)
    else:
        if not args.dsn:
            print("错误：MySQL 模式需要 --dsn")
            return 1
        generate_for_mysql(args.dsn)

    return 0


if __name__ == "__main__":
    sys.exit(main())
