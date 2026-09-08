PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS stores (
  store_id INTEGER PRIMARY KEY, store_name TEXT NOT NULL, city TEXT NOT NULL,
  region TEXT NOT NULL, store_type TEXT NOT NULL, opened_at TEXT NOT NULL, is_active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS customers (
  customer_id INTEGER PRIMARY KEY, customer_name TEXT NOT NULL, gender TEXT NOT NULL,
  age INTEGER NOT NULL, city TEXT NOT NULL, region TEXT NOT NULL, customer_level TEXT NOT NULL,
  registered_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS products (
  product_id INTEGER PRIMARY KEY, sku_code TEXT UNIQUE NOT NULL, product_name TEXT NOT NULL,
  brand TEXT NOT NULL, category TEXT NOT NULL, cost_price NUMERIC NOT NULL,
  sale_price NUMERIC NOT NULL, list_price NUMERIC NOT NULL, launched_at TEXT NOT NULL, is_active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS promotions (
  promotion_id INTEGER PRIMARY KEY, promotion_name TEXT NOT NULL, promotion_type TEXT NOT NULL,
  start_at TEXT NOT NULL, end_at TEXT NOT NULL, min_amount NUMERIC NOT NULL DEFAULT 0,
  discount_value NUMERIC NOT NULL, max_discount NUMERIC, is_active INTEGER NOT NULL DEFAULT 1
);
CREATE TABLE IF NOT EXISTS orders (
  order_id INTEGER PRIMARY KEY, order_no TEXT UNIQUE NOT NULL, customer_id INTEGER NOT NULL,
  store_id INTEGER NOT NULL, order_status TEXT NOT NULL, order_amount NUMERIC NOT NULL,
  discount_amount NUMERIC NOT NULL DEFAULT 0, freight_amount NUMERIC NOT NULL DEFAULT 0,
  paid_amount NUMERIC NOT NULL, cost_amount NUMERIC NOT NULL, profit_amount NUMERIC NOT NULL,
  item_count INTEGER NOT NULL, channel TEXT NOT NULL, promotion_id INTEGER,
  created_at TEXT NOT NULL, paid_at TEXT, shipped_at TEXT, delivered_at TEXT, completed_at TEXT, cancelled_at TEXT,
  FOREIGN KEY(customer_id) REFERENCES customers(customer_id), FOREIGN KEY(store_id) REFERENCES stores(store_id), FOREIGN KEY(promotion_id) REFERENCES promotions(promotion_id)
);
CREATE TABLE IF NOT EXISTS order_items (
  item_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, product_id INTEGER NOT NULL,
  sku_code TEXT NOT NULL, brand TEXT NOT NULL, category TEXT NOT NULL, quantity INTEGER NOT NULL,
  unit_price NUMERIC NOT NULL, unit_cost NUMERIC NOT NULL, discount_amount NUMERIC NOT NULL DEFAULT 0,
  subtotal_amount NUMERIC NOT NULL, subtotal_cost NUMERIC NOT NULL, line_paid_amount NUMERIC NOT NULL, subtotal_profit NUMERIC NOT NULL,
  FOREIGN KEY(order_id) REFERENCES orders(order_id), FOREIGN KEY(product_id) REFERENCES products(product_id)
);
CREATE TABLE IF NOT EXISTS payments (
  payment_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, payment_method TEXT NOT NULL,
  payment_amount NUMERIC NOT NULL, payment_status TEXT NOT NULL, refund_amount NUMERIC NOT NULL DEFAULT 0,
  paid_at TEXT, transaction_id TEXT UNIQUE, FOREIGN KEY(order_id) REFERENCES orders(order_id)
);
CREATE TABLE IF NOT EXISTS refunds (
  refund_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, payment_id INTEGER NOT NULL,
  refund_reason TEXT NOT NULL, refund_type TEXT NOT NULL, refund_amount NUMERIC NOT NULL,
  refund_status TEXT NOT NULL, requested_at TEXT NOT NULL, completed_at TEXT,
  FOREIGN KEY(order_id) REFERENCES orders(order_id), FOREIGN KEY(payment_id) REFERENCES payments(payment_id)
);
CREATE TABLE IF NOT EXISTS inventory_snapshots (
  store_id INTEGER NOT NULL, product_id INTEGER NOT NULL, snapshot_date TEXT NOT NULL,
  quantity_on_hand INTEGER NOT NULL, quantity_reserved INTEGER NOT NULL, quantity_available INTEGER NOT NULL,
  reorder_level INTEGER NOT NULL, PRIMARY KEY(store_id, product_id, snapshot_date),
  FOREIGN KEY(store_id) REFERENCES stores(store_id), FOREIGN KEY(product_id) REFERENCES products(product_id)
);
CREATE TABLE IF NOT EXISTS after_sales (
  ticket_id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, customer_id INTEGER NOT NULL,
  ticket_type TEXT NOT NULL, ticket_status TEXT NOT NULL, priority TEXT NOT NULL, assigned_to TEXT,
  created_at TEXT NOT NULL, first_response_at TEXT, resolved_at TEXT, closed_at TEXT,
  response_time_minutes INTEGER, resolution_time_hours NUMERIC, satisfaction_score INTEGER,
  FOREIGN KEY(order_id) REFERENCES orders(order_id), FOREIGN KEY(customer_id) REFERENCES customers(customer_id)
);

CREATE INDEX IF NOT EXISTS idx_orders_created ON orders(created_at);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON orders(customer_id);
CREATE INDEX IF NOT EXISTS idx_orders_store ON orders(store_id);
CREATE INDEX IF NOT EXISTS idx_items_product ON order_items(product_id);
CREATE INDEX IF NOT EXISTS idx_refunds_requested ON refunds(requested_at);
CREATE INDEX IF NOT EXISTS idx_inventory_date ON inventory_snapshots(snapshot_date);
CREATE INDEX IF NOT EXISTS idx_after_sales_created ON after_sales(created_at);
