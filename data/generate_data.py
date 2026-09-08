"""Generate deterministic demo data for Enterprise Data Agent.

Usage: python data/generate_data.py --db data/enterprise.db --seed 20260907
"""
from __future__ import annotations
import argparse, csv, random, sqlite3
from datetime import datetime, timedelta
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SCHEMA = ROOT / "init.sql"
Q = lambda x: float(Decimal(str(x)).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP))

BRANDS = ["Nova", "Mira", "Aster", "Pulse", "Vertex", "Lumen", "Orbit", "Cedar"]
CATEGORIES = ["手机", "平板", "耳机", "智能穿戴", "电脑配件", "家居数码"]
CITIES = [("长沙", "华中"), ("武汉", "华中"), ("广州", "华南"), ("深圳", "华南"), ("杭州", "华东"), ("成都", "西南"), ("西安", "西北"), ("北京", "华北")]

def dt(s): return datetime.strptime(s, "%Y-%m-%d %H:%M:%S")
def iso(d): return d.strftime("%Y-%m-%d %H:%M:%S")

def generate(db: Path, seed=20260907, stores_n=20, customers_n=10000, products_n=1500, orders_n=50000):
    rng = random.Random(seed); db.parent.mkdir(parents=True, exist_ok=True)
    con = sqlite3.connect(db); con.execute("PRAGMA foreign_keys=ON"); con.executescript(SCHEMA.read_text(encoding="utf-8"))
    tables = ["after_sales","refunds","payments","order_items","orders","inventory_snapshots","promotions","products","customers","stores"]
    with con:
        for t in tables: con.execute(f"DELETE FROM {t}")
        stores=[]
        for i in range(1, stores_n+1):
            city, region = CITIES[(i-1)%len(CITIES)]
            stores.append((i,f"{city}{i:02d}号店",city,region,"直营" if i%3 else "加盟", "2023-01-01",1))
        con.executemany("INSERT INTO stores VALUES (?,?,?,?,?,?,?)", stores)
        customers=[]
        for i in range(1, customers_n+1):
            city, region=rng.choice(CITIES); reg=dt("2024-01-01 00:00:00")+timedelta(days=rng.randrange(500))
            customers.append((i,f"客户{i:05d}",rng.choice(["男","女"]),rng.randint(18,65),city,region,rng.choices(["普通","银卡","金卡","黑卡"],[55,25,15,5])[0],iso(reg)))
        con.executemany("INSERT INTO customers VALUES (?,?,?,?,?,?,?,?)",customers)
        products=[]
        for i in range(1,products_n+1):
            brand=rng.choice(BRANDS); cat=rng.choice(CATEGORIES); cost=Q(rng.uniform(20,3200)); sale=Q(cost*rng.uniform(1.15,1.65)); launch=dt("2025-07-01 00:00:00")+timedelta(days=rng.randrange(365))
            products.append((i,f"SKU-{i:05d}",f"{brand}{cat}{i:04d}",brand,cat,cost,sale,Q(sale*rng.uniform(1.05,1.35)),iso(launch),1))
        con.executemany("INSERT INTO products VALUES (?,?,?,?,?,?,?,?,?,?)",products)
        p=[]
        for i,(name,start,end,val) in enumerate([("618大促","2026-06-01","2026-06-20",0.10),("暑期优惠","2026-07-01","2026-07-31",0.08),("开学季","2026-08-15","2026-09-15",0.12),("双11大促","2026-11-01","2026-11-15",0.15)],1): p.append((i,name,"满减",start+" 00:00:00",end+" 23:59:59",100,val,200,1))
        con.executemany("INSERT INTO promotions VALUES (?,?,?,?,?,?,?,?,?)",p)
        base=dt("2025-09-01 00:00:00"); order_rows=[]; item_rows=[]; pay_rows=[]; refund_rows=[]; after_rows=[]; item_id=1; payment_id=1; refund_id=1; ticket_id=1
        for oid in range(1,orders_n+1):
            created=base+timedelta(minutes=rng.randrange(365*24*60)); customer=rng.randint(1,customers_n); store=rng.randint(1,stores_n); n=rng.randint(1,4); chosen=[rng.randint(1,products_n) for _ in range(n)]
            status=rng.choices(["completed","delivered","shipped","paid","cancelled"],[62,12,8,10,8])[0]; paid=created+timedelta(minutes=rng.randint(2,60)) if status!="created" else None; shipped=paid+timedelta(hours=rng.randint(2,36)) if paid and status not in ("paid","cancelled") else None; delivered=shipped+timedelta(days=rng.randint(1,5)) if shipped and status not in ("shipped","cancelled") else None; completed=delivered+timedelta(days=rng.randint(0,3)) if delivered and status=="completed" else None; cancelled=created+timedelta(hours=rng.randint(1,48)) if status=="cancelled" else None
            lines=[]; gross=cost_total=0
            for pid in chosen:
                pr=products[pid-1]; qty=rng.randint(1,2); amount=Q(pr[6]*qty); cost=Q(pr[5]*qty); lines.append((pid,pr,qty,amount,cost)); gross+=amount; cost_total+=cost
            promo_id=rng.choice([None,None,None,1,2,3,4]); discount=Q(gross*([0,.05,.08,.1,.12,.15][rng.randrange(6)])) if promo_id else 0; freight=0 if gross>=200 else 8; paid_amount=Q(gross-discount+freight) if paid else 0; profit=Q(paid_amount-cost_total) if paid else 0
            order_rows.append((oid,f"EA{created:%Y%m%d}{oid:06d}",customer,store,status,Q(gross),discount,freight,paid_amount,Q(cost_total),profit,n,rng.choice(["门店","小程序","电商平台"]),promo_id,iso(created),iso(paid) if paid else None,iso(shipped) if shipped else None,iso(delivered) if delivered else None,iso(completed) if completed else None,iso(cancelled) if cancelled else None))
            for pid,pr,qty,amount,cost in lines:
                share=amount/gross if gross else 0; disc=Q(discount*share); line_paid=Q(amount-disc); item_rows.append((item_id,oid,pid,pr[1],pr[3],pr[4],qty,pr[6],pr[5],disc,amount,cost,line_paid,Q(line_paid-cost))); item_id+=1
            if paid: pay_rows.append((payment_id,oid,rng.choice(["微信","支付宝","银行卡"]),paid_amount,"success",0,iso(paid),f"TX{oid:010d}")); payment_id+=1
            if paid and (status=="cancelled" or (delivered and rng.random()<.07)):
                amount=paid_amount if status=="cancelled" else Q(paid_amount*rng.uniform(.2,1)); requested=(cancelled or delivered)+timedelta(days=rng.randint(1,30)); completed_r=requested+timedelta(hours=rng.randint(2,72)); refund_rows.append((refund_id,oid,payment_id-1,"主动取消" if status=="cancelled" else "质量问题","全额" if amount==paid_amount else "部分",amount,"completed",iso(requested),iso(completed_r))); refund_id+=1
            if rng.random()<.06 and paid:
                ca=(delivered or paid)+timedelta(hours=rng.randint(1,48)); fr=ca+timedelta(minutes=rng.randint(5,240)); re=fr+timedelta(hours=rng.randint(2,120)) if rng.random()<.8 else None; cl=re+timedelta(hours=rng.randint(1,48)) if re and rng.random()<.9 else None; after_rows.append((ticket_id,oid,customer,rng.choice(["退款","换货","物流","商品咨询"]),"closed" if cl else ("resolved" if re else "open"),rng.choice(["low","medium","high"]),f"客服{rng.randint(1,30):02d}",iso(ca),iso(fr) if fr else None,iso(re) if re else None,iso(cl) if cl else None,int((fr-ca).total_seconds()/60) if fr else None,Q((re-ca).total_seconds()/3600) if re else None,rng.randint(3,5) if cl else None)); ticket_id+=1
        con.executemany("INSERT INTO orders VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)",order_rows); con.executemany("INSERT INTO order_items VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",item_rows); con.executemany("INSERT INTO payments VALUES (?,?,?,?,?,?,?,?)",pay_rows); con.executemany("INSERT INTO refunds VALUES (?,?,?,?,?,?,?,?,?)",refund_rows); con.executemany("INSERT INTO after_sales VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",after_rows)
        inv=[]; snap_dates=[dt("2025-09-01 00:00:00")+timedelta(days=15*i) for i in range(24)]
        for s in range(1,stores_n+1):
            active=rng.sample(range(1,products_n+1), min(400,products_n))
            for d in snap_dates:
                for pid in active:
                    on=rng.randint(0,220); reserved=rng.randint(0,min(20,on)); inv.append((s,pid,d.date().isoformat(),on,reserved,on-reserved,rng.randint(10,50)))
        con.executemany("INSERT INTO inventory_snapshots VALUES (?,?,?,?,?,?,?)",inv)
    con.close(); print(f"generated {orders_n:,} orders, {len(item_rows):,} items, {len(inv):,} inventory rows -> {db}")

if __name__ == "__main__":
    ap=argparse.ArgumentParser(); ap.add_argument("--db", type=Path, default=ROOT/"enterprise.db"); ap.add_argument("--seed", type=int, default=20260907); ap.add_argument("--orders", type=int, default=50000); args=ap.parse_args(); generate(args.db,args.seed,orders_n=args.orders)
