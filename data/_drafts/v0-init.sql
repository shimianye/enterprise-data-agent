-- ============================================================
-- 企业经营数据分析 Agent - 数据库 Schema
-- MySQL 8.0+ / SQLite 兼容
-- 9 张核心表，覆盖商品、订单、物流、售后、库存全链路
-- ============================================================

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ------------------------------------------------------------
-- 1. 门店表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS stores;
CREATE TABLE stores (
    store_id        INT             PRIMARY KEY,
    store_name      VARCHAR(64)     NOT NULL COMMENT '门店名称，如 长沙五一广场旗舰店',
    city            VARCHAR(32)     NOT NULL COMMENT '所在城市',
    region          VARCHAR(32)     NOT NULL COMMENT '所属区域：华中/华东/华南/华北/西南/西北/东北',
    store_type      VARCHAR(16)     NOT NULL COMMENT '门店类型：直营/加盟/体验店',
    opened_at       DATE            NOT NULL COMMENT '开业日期',
    is_active       TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '是否营业中'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='门店信息表';

-- ------------------------------------------------------------
-- 2. 商品类目表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS categories;
CREATE TABLE categories (
    category_id     INT             PRIMARY KEY,
    category_name   VARCHAR(32)     NOT NULL COMMENT '类目名称',
    parent_id       INT             DEFAULT NULL COMMENT '父类目 ID',
    level           TINYINT         NOT NULL COMMENT '层级：1-大类 2-中类 3-小类',
    sort_order      INT             NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品类目表';

-- ------------------------------------------------------------
-- 3. 商品表（含 SKU）
-- ------------------------------------------------------------
DROP TABLE IF EXISTS products;
CREATE TABLE products (
    product_id      INT             PRIMARY KEY,
    sku_code        VARCHAR(32)     NOT NULL UNIQUE COMMENT 'SKU 编码',
    product_name    VARCHAR(128)    NOT NULL COMMENT '商品名称',
    brand           VARCHAR(32)     NOT NULL COMMENT '品牌：Apple/华为/小米/OPPO/vivo/三星/其他',
    category_id     INT             NOT NULL COMMENT '所属类目',
    cost_price      DECIMAL(10,2)   NOT NULL COMMENT '成本价',
    sale_price      DECIMAL(10,2)   NOT NULL COMMENT '建议零售价',
    is_active       TINYINT(1)      NOT NULL DEFAULT 1 COMMENT '是否在售',
    created_at      DATETIME        NOT NULL COMMENT '上架时间',
    KEY idx_brand (brand),
    KEY idx_category (category_id),
    KEY idx_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='商品 SKU 表';

-- ------------------------------------------------------------
-- 4. 客户表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS customers;
CREATE TABLE customers (
    customer_id     INT             PRIMARY KEY,
    customer_name   VARCHAR(64)     NOT NULL COMMENT '客户姓名',
    gender          CHAR(1)         COMMENT 'M/F',
    age             TINYINT         COMMENT '年龄',
    city            VARCHAR(32)     NOT NULL COMMENT '所在城市',
    customer_level  VARCHAR(16)     NOT NULL DEFAULT '普通' COMMENT '客户等级：普通/银卡/金卡/铂金',
    registered_at   DATETIME        NOT NULL COMMENT '注册时间',
    is_active       TINYINT(1)      NOT NULL DEFAULT 1,
    KEY idx_city (city),
    KEY idx_level (customer_level),
    KEY idx_registered (registered_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='客户信息表';

-- ------------------------------------------------------------
-- 5. 订单表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS orders;
CREATE TABLE orders (
    order_id        BIGINT          PRIMARY KEY,
    order_no        VARCHAR(32)     NOT NULL UNIQUE COMMENT '订单编号',
    customer_id     INT             NOT NULL,
    store_id        INT             NOT NULL COMMENT '下单门店',
    order_status    VARCHAR(16)     NOT NULL COMMENT '订单状态：created/paid/shipped/completed/cancelled',
    order_amount    DECIMAL(10,2)   NOT NULL COMMENT '订单总金额（含运费前）',
    discount_amount DECIMAL(10,2)   NOT NULL DEFAULT 0 COMMENT '优惠金额',
    freight_amount  DECIMAL(10,2)   NOT NULL DEFAULT 0 COMMENT '运费',
    paid_amount     DECIMAL(10,2)   NOT NULL DEFAULT 0 COMMENT '实付金额',
    item_count      INT             NOT NULL COMMENT '商品件数',
    channel         VARCHAR(16)     NOT NULL COMMENT '渠道：app/miniprogram/web/offline',
    created_at      DATETIME        NOT NULL COMMENT '下单时间',
    paid_at         DATETIME        COMMENT '支付时间',
    shipped_at      DATETIME        COMMENT '发货时间',
    completed_at    DATETIME        COMMENT '完成时间',
    cancelled_at    DATETIME        COMMENT '取消时间',
    KEY idx_customer (customer_id),
    KEY idx_store (store_id),
    KEY idx_status (order_status),
    KEY idx_created (created_at),
    KEY idx_paid (paid_at),
    KEY idx_channel (channel)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单主表';

-- ------------------------------------------------------------
-- 6. 订单明细表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS order_items;
CREATE TABLE order_items (
    item_id         BIGINT          PRIMARY KEY,
    order_id        BIGINT          NOT NULL,
    product_id      INT             NOT NULL,
    sku_code        VARCHAR(32)     NOT NULL,
    product_name    VARCHAR(128)    NOT NULL COMMENT '冗余：下单时商品名',
    brand           VARCHAR(32)     NOT NULL,
    quantity        INT             NOT NULL COMMENT '购买数量',
    unit_price      DECIMAL(10,2)   NOT NULL COMMENT '成交单价',
    subtotal_amount DECIMAL(10,2)   NOT NULL COMMENT '小计金额',
    KEY idx_order (order_id),
    KEY idx_product (product_id),
    KEY idx_brand (brand)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='订单明细表';

-- ------------------------------------------------------------
-- 7. 支付记录表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS payments;
CREATE TABLE payments (
    payment_id      BIGINT          PRIMARY KEY,
    order_id        BIGINT          NOT NULL,
    payment_method  VARCHAR(16)     NOT NULL COMMENT '支付方式：wechat/alipay/card/installment',
    payment_amount  DECIMAL(10,2)   NOT NULL,
    paid_at         DATETIME        NOT NULL,
    transaction_id  VARCHAR(64)     NOT NULL UNIQUE COMMENT '第三方交易号',
    KEY idx_order (order_id),
    KEY idx_paid (paid_at),
    KEY idx_method (payment_method)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='支付流水表';

-- ------------------------------------------------------------
-- 8. 退款表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS refunds;
CREATE TABLE refunds (
    refund_id       BIGINT          PRIMARY KEY,
    order_id        BIGINT          NOT NULL,
    payment_id      BIGINT          NOT NULL,
    refund_reason   VARCHAR(64)     NOT NULL COMMENT '退款原因：质量问题/不想要了/物流问题/其他',
    refund_type     VARCHAR(16)     NOT NULL COMMENT '仅退款/退货退款/换货',
    refund_amount   DECIMAL(10,2)   NOT NULL,
    refund_status   VARCHAR(16)     NOT NULL COMMENT '退款状态：requested/approved/rejected/completed',
    requested_at    DATETIME        NOT NULL,
    completed_at    DATETIME        COMMENT '退款完成时间',
    KEY idx_order (order_id),
    KEY idx_status (refund_status),
    KEY idx_requested (requested_at),
    KEY idx_reason (refund_reason)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='售后退款表';

-- ------------------------------------------------------------
-- 9. 库存变动日志表
-- ------------------------------------------------------------
DROP TABLE IF EXISTS inventory_logs;
CREATE TABLE inventory_logs (
    log_id          BIGINT          PRIMARY KEY,
    store_id        INT             NOT NULL,
    product_id      INT             NOT NULL,
    change_type     VARCHAR(16)     NOT NULL COMMENT '变动类型：inbound/outbound/adjustment/return',
    change_qty      INT             NOT NULL COMMENT '变动数量（正为入，负为出）',
    stock_after     INT             NOT NULL COMMENT '变动后库存',
    reference_no    VARCHAR(32)     COMMENT '关联单号：PO/SO/Refund',
    created_at      DATETIME        NOT NULL,
    KEY idx_store (store_id),
    KEY idx_product (product_id),
    KEY idx_created (created_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='库存变动流水表';

SET FOREIGN_KEY_CHECKS = 1;

-- ============================================================
-- 索引补强：跨表分析常用组合
-- ============================================================
CREATE INDEX idx_orders_status_paid ON orders(order_status, paid_at);
CREATE INDEX idx_items_brand_order ON order_items(brand, order_id);
CREATE INDEX idx_refunds_completed ON refunds(refund_status, completed_at);
