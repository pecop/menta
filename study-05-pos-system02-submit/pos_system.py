import pandas as pd
import datetime
import os
import eel

### 商品クラス
class Item:
    def __init__(self,item_code,item_name,price):
        self.item_code=item_code
        self.item_name=item_name
        self.price=price
    
    def get_price(self):
        return self.price

### オーダークラス
class Order:
    def __init__(self,item_master):
        self.item_order_list=[]
        self.item_unit_list=[]
        self.item_master=item_master
    
    def input_order_item_code(self, item_code):
        try:
            m_item_code_list = [m_item.item_code for m_item in self.item_master]
            m_item_code_list.sort()
            order_code = item_code
            if order_code in m_item_code_list:    
                return order_code    
            else:
                eel.view_log_js(f"商品コードを{m_item_code_list[0]}〜{m_item_code_list[-1]}の値で入力してください\n")
        except:
            eel.view_log_js(f"\商品コードを{m_item_code_list[0]}〜{m_item_code_list[-1]}の値で入力してください\n")

    def input_order_item_unit(self, item_unit):
        try:
            order_unit = int(item_unit)
            if order_unit > 0:
                return order_unit
            else:
                eel.view_log_js("個数を1以上の整数で入力してください\n")
        except:
            eel.view_log_js("個数を1以上の整数で入力してください\n")

    def add_item_order(self,item_code, item_unit):
        self.item_code = item_code
        self.item_order_list.append(item_code)
        self.item_unit = item_unit
        self.item_unit_list.append(item_unit)
    
    def get_item_data(self):
        self.sum_price = 0
        self.sum_unit = 0
        self.receipt_dic = {}
        for m_item in self.item_master:
            for item_code, item_unit in zip(self.item_order_list, self.item_unit_list):
                if item_code == m_item.item_code:
                    self.sum_price += int(m_item.price) * item_unit
                    self.sum_unit += item_unit
                    self.receipt_dic = {
                        "商品名": m_item.item_name,
                        "単価": m_item.price,
                        "注文数": self.sum_unit,
                        "合計金額": self.sum_price
                    }
        eel.view_log_js('\n【注文内容】')
        eel.view_log_js(f'商品名: {self.receipt_dic["商品名"]}')
        eel.view_log_js(f'単価: {self.receipt_dic["単価"]}円')
        eel.view_log_js(f'注文数: {self.receipt_dic["注文数"]}個')
        eel.view_log_js(f'合計金額: {self.receipt_dic["合計金額"]}円')

    def input_payment(self, payment):
        payment = int(payment)
        try:
            if payment >= self.sum_price:
                eel.view_log_js('\n【会計】')
                eel.view_log_js(f'合計金額: {self.sum_price}円')
                eel.view_log_js(f"支払い金額:　{payment}円")
                return payment
            else:
                eel.view_log_js(f"支払い金額を合計金額:{self.sum_price}円以上の整数で入力してください")   
        except:
            eel.view_log_js(f"支払い金額を合計金額:{self.sum_price}円以上の整数で入力してください")

    def calc_change(self, payment):
        self.payment = payment
        change = payment - self.sum_price
        eel.view_log_js(f"お釣り:　{change}円")
        return change

    def output_receipt(self, change):
        self.change = change
        self.receipt_dic["お釣り"] = self.change
        receipt = pd.DataFrame(self.receipt_dic, index=["i",])
        receipt.to_csv(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.txt", index=False, encoding="utf-8-sig")
    
def get_item_master_from_csv(csv_file):
    csv_file_path = os.path.join(os.getcwd(), csv_file)
    item_master=[]
    if os.path.exists(csv_file_path):
        try:
            read_item_master = pd.read_csv(csv_file_path, dtype=object)
        except:
            eel.view_log_js(f"入力されたcsvファイルは存在しません\n")
    else:
        eel.view_log_js(f"入力されたcsvファイルは存在しません\n")
    eel.view_log_js('【商品マスター】')
    for item_code, item_name, price in zip(read_item_master['item_code'], read_item_master['item_name'], read_item_master['price']):
        eel.view_log_js(f'{item_code}' + ' ' + f'{item_name}' + ' ' + f'{price}円')
        item_master.append(Item(item_code, item_name, price))
    return item_master

### メイン処理
# 商品登録処理    
def process_item_master_registration(csv_file):
    # 商品マスタ登録
    global item_master
    item_master = get_item_master_from_csv(csv_file)

## 注文処理
def process_order(item_code, item_unit):   
    global order
    order = Order(item_master)
    order_code = order.input_order_item_code(item_code)
    order_unit = order.input_order_item_unit(item_unit)
    order.add_item_order(order_code, order_unit) 
    order.get_item_data()
    
## 精算処理
def process_settlement(payment):
    # 支払い金額取得/表示
    payment = order.input_payment(payment)
    # お釣り計算/表示
    change = order.calc_change(payment)
    # レシート出力
    order.output_receipt(change)