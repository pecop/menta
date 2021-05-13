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
                print(f"商品コードを{m_item_code_list[0]}〜{m_item_code_list[-1]}の値で入力してください")
                eel.view_log_js(f"商品コードを{m_item_code_list[0]}〜{m_item_code_list[-1]}の値で入力してください")
        except:
            print(f"商品コードを{m_item_code_list[0]}〜{m_item_code_list[-1]}の値で入力してください")
            eel.view_log_js(f"商品コードを{m_item_code_list[0]}〜{m_item_code_list[-1]}の値で入力してください")

    def input_order_item_unit(self, item_unit):
        try:
            order_unit = int(item_unit)
            if order_unit > 0:
                return order_unit
            else:
                print("個数を1以上の整数で入力してください")
                eel.view_log_js("個数を1以上の整数で入力してください")
        except:
            print("個数を1以上の整数で入力してください")
            eel.view_log_js("個数を1以上の整数で入力してください")

    def add_item_order(self,item_code, item_unit):
        self.item_code = item_code
        self.item_order_list.append(item_code)
        self.item_unit = item_unit
        self.item_unit_list.append(item_unit)

    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item))
    
    def get_item_data(self):
        self.sum_price = 0
        self.sum_unit = 0
        self.receipt_dic = {}
        for m_item in self.item_master:
            for item_code, item_unit in zip(self.item_order_list, self.item_unit_list):
                if item_code == m_item.item_code:
                    print(f'注文した商品: {m_item.item_name}, {m_item.price}円')
                    self.sum_price += int(m_item.price) * item_unit
                    self.sum_unit += item_unit
                    self.receipt_dic = {
                        "商品名": m_item.item_name,
                        "単価": m_item.price,
                        "注文数": self.sum_unit,
                        "合計金額": self.sum_price
                    }
        print(f'【注文内容】')
        eel.view_log_js('【注文内容】')
        print(f'商品名: {m_item.item_name}')
        eel.view_log_js(f'商品名: {m_item.item_name}')
        print(f'単価: {m_item.price}円')
        eel.view_log_js(f'単価: {m_item.price}円')
        print(f'注文数: {self.sum_unit}個')
        eel.view_log_js(f'注文数: {self.sum_unit}個')
        print(f'合計金額: {self.sum_price}円')
        eel.view_log_js(f'合計金額: {self.sum_price}円')

    def input_payment(self, payment):
        while True:
            try:
                if payment >= self.sum_price:
                    eel.view_log_js(f'合計金額: {self.sum_price}円')
                    eel.view_log_js(f"支払い金額:　{payment}円")
                    return payment
                    break
                else:
                    print(f"支払い金額を合計金額:{self.sum_price}円以上の整数で入力してください")
                    eel.view_log_js(f"支払い金額を合計金額:{self.sum_price}円以上の整数で入力してください")   
            except:
                print(f"支払い金額を合計金額:{self.sum_price}円以上の整数で入力してください")
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
    try:
        read_item_master = pd.read_csv(csv_file_path, dtype=object)
        print("csvファイルを読み込めました")
    except:
        print("csvファイルを読み込めませんでした")
    for item_code, item_name, price in zip(read_item_master['item_code'], read_item_master['item_name'], read_item_master['price']):
        print(item_code, item_name, price)
        item_master.append(Item(item_code, item_name, price))
    return item_master

### メイン処理
# def main_process(csv_file, item_code, item_unit, payment):
#     ## 注文処理
#     if item_code and item_unit:
#     # def process_order(csv_file, item_code, item_unit):
#         # 商品マスタ登録
#         item_master = get_item_master_from_csv(csv_file)
#         # 注文登録/表示
#         order=Order(item_master)
#         order_code = order.input_order_item_code(item_code)
#         order_unit = order.input_order_item_unit(item_unit)
#         order.add_item_order(order_code, order_unit) 
#         order.get_item_data()
#         # return order
    
#     ## 精算処理
#     elif payment:
#     # def process_settlement(payment, order):
#         # 支払い金額取得/表示
#         payment = order.input_payment(payment)
#         # お釣り計算/表示
#         change = order.calc_change(payment)
#         # レシート出力
#         order.output_receipt(change)

### メイン処理    
## 注文処理
def process_order(csv_file, item_code, item_unit):
    # 商品マスタ登録
    item_master = get_item_master_from_csv(csv_file)
    # 注文登録/表示
    order=Order(item_master)
    order_code = order.input_order_item_code(item_code)
    order_unit = order.input_order_item_unit(item_unit)
    order.add_item_order(order_code, order_unit) 
    order.get_item_data()
    return order
    
## 精算処理
def process_settlement(payment, order):
    print("精算スタート")
    # 支払い金額取得/表示
    payment = order.input_payment(payment)
    # お釣り計算/表示
    change = order.calc_change(payment)
    # レシート出力
    order.output_receipt(change)

