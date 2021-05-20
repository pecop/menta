import eel
import desktop
import pos_system

app_name="html"
end_point="index.html"
# size=(700,600)
size=(900,1000)


@eel.expose
def process_item_master_registration(csv_file):
    pos_system.process_item_master_registration(csv_file)

@eel.expose
def process_order(item_code, item_unit):
    pos_system.process_order(item_code, item_unit)

@eel.expose
def process_settlement(payment):
    pos_system.process_settlement(payment)
    
desktop.start(app_name,end_point,size)