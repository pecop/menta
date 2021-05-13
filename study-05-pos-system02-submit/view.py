import eel
import desktop
# import search
import pos_system

app_name="html"
end_point="index.html"
size=(700,600)

# @eel.expose
# def main_process(csv_file=None, item_code=None, item_unit=None, payment=None):
#     pos_system.main_process(csv_file, item_code, item_unit, payment)

@eel.expose
def process_order(csv_file=None, item_code=None, item_unit=None):
    order = pos_system.process_order(csv_file, item_code, item_unit)
    # pos_system.process_order(csv_file, item_code, item_unit)
    return order

@eel.expose
def process_settlement(payment, order):
    pos_system.process_settlement(payment, order)
    
desktop.start(app_name,end_point,size)
#desktop.start(size=size,appName=app_name,endPoint=end_point)