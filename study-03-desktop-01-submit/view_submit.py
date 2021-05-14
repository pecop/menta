import eel
import desktop
import search_submit

app_name="html"
end_point="index_submit.html"
size=(700,600)

# STEP6
@ eel.expose
def kimetsu_search(word, csv_file):
    search_submit.kimetsu_search(word, csv_file)
    
desktop.start(app_name,end_point,size)