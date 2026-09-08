TABLE_DESCRIPTIONS = {
    "stores": "门店维度，region 为大区，store_type 为直营或加盟",
    "customers": "客户维度，customer_level 为客户等级",
    "products": "商品维度，cost_price 为内部成本价，sale_price 为标价销售价",
    "orders": "订单事实，paid_amount 为订单实付金额，profit_amount 为订单利润汇总",
    "order_items": "订单明细事实，line_paid_amount 为明细实付金额，subtotal_profit 为明细利润",
    "payments": "支付资金事实，payment_status=success 表示支付成功",
    "refunds": "退款资金事实，refund_status=completed 表示退款成功；用于退款率",
    "inventory_snapshots": "门店商品库存月度快照，quantity_available 为可用库存",
    "promotions": "促销活动维度，订单通过 promotion_id 关联一项主促销",
    "after_sales": "售后服务工单事实，不等同于 refunds 资金退款事实",
}
