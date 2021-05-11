import pandas as pd
import datetime

CSV_FILE_PATH = './item_master.csv'

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
        # SETP4
        self.item_unit_list=[]
        self.item_master=item_master
    
    # STEP2
    def input_order_item_code(self):
        while True:
            try:
                m_item_code_list = [m_item.item_code for m_item in self.item_master].sort()
                order_code = input(f"オーダーの商品コードを登録してください（商品コード:{m_item_code_list[0]}〜{m_item_code_list[-1]}）>>")
                if order_code in m_item_code_list:    
                    return order_code
                    break    
                else:
                    print(f"商品コードを{m_item_code_list[0]}〜{m_item_code_list[-1]}の値で入力してください")  
            except:
                print(f"商品コードを{m_item_code_list[0]}〜{m_item_code_list[-1]}の値で入力してください")

    # STEP4
    def get_input_order_item_unit(self):
        while True:
            try:
                order_unit = int(input("オーダーの個数を登録してください（個数：1〜）>>"))
                if order_unit > 0:
                    return order_unit
                    break
                else:
                    print("個数を1以上の整数で入力してください")   
            except:
                print("個数を1以上の整数で入力してください")

    # SETP4
    def add_item_order(self,item_code, item_unit):
        self.item_code = item_code
        self.item_order_list.append(item_code)
        # SETP4
        self.item_unit = item_unit
        self.item_unit_list.append(item_unit)

    def view_item_list(self):
        for item in self.item_order_list:
            print("商品コード:{}".format(item))
    
    # STEP1 #STEP3 #STEP5
    def get_item_data(self):
        self.sum_price = 0
        self.sum_unit = 0
        # STEP7
        self.receipt_dic = {}
        for m_item in self.item_master:
            for item_code, item_unit in zip(self.item_order_list, self.item_unit_list):
                if item_code == m_item.item_code:
                    print(f'オーダー登録した商品: {m_item.item_name}, {m_item.price}円')
                    self.sum_price += int(m_item.price) * item_unit
                    self.sum_unit += item_unit
                    self.receipt_dic = {
                        "商品名": m_item.item_name,
                        "価格": m_item.price,
                        "合計金額": self.sum_price,
                        "個数": self.sum_unit
                    }
        print(f'合計金額: {self.sum_price}')
        print(f'合計個数: {self.sum_unit}')

    def get_input_pay(self):
        while True:
            try:
                pay = int(input("支払い金額を入力してください（金額：1〜）>>"))
                if pay >= self.sum_price:
                    return pay
                    break
                else:
                    print(f"支払い金額を合計金額:{self.sum_price}円以上の整数で入力してください")   
            except:
                print(f"支払い金額を合計金額:{self.sum_price}円以上の整数で入力してください")

    # STEP6
    def calc_change(self, pay):
        self.pay = pay
        change = pay - self.sum_price
        return change

    def output_receipt(self, change):
        self.change = change
        self.receipt_dic["お釣り"] = self.change
        receipt = pd.DataFrame(self.receipt_dic, index=["i",])
        receipt.to_csv(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.txt", index=False, encoding="utf-8-sig")
    
# STEP3
def get_item_master_from_csv(csv_file_path):
    item_master=[]
    read_item_master = pd.read_csv(csv_file_path, dtype=object)
    for item_code, item_name, price in zip(read_item_master['item_code'], read_item_master['item_name'], read_item_master['price']):
        print(item_code, item_name, price)
        item_master.append(Item(item_code, item_name, price))
    return item_master

### メイン処理
def main():
    # マスタ登録
    # item_master=[]
    # item_master.append(Item("001","りんご",100))
    # item_master.append(Item("002","なし",120))
    # item_master.append(Item("003","みかん",150))

    # STEP3
    item_master = get_item_master_from_csv(CSV_FILE_PATH)

    # オーダー登録
    order=Order(item_master)
    # order.add_item_order("001")
    # order.add_item_order("002")
    # order.add_item_order("003")

    # STEP2 
    order_code = order.input_order_item_code()
    # #STEP4
    order_unit = order.get_input_order_item_unit()

    order.add_item_order(order_code, order_unit)

    # オーダー表示
    # order.view_item_list()
    
    # STEP1
    order.get_item_data()
    # STEP6
    pay = order.get_input_pay()
    change = order.calc_change(pay)
    # STEP7
    order.output_receipt(change)

if __name__ == "__main__":
    main()