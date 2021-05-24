import eel
import desktop
import googletrans_api

app_name="html"
end_point="index.html"
size=(900,1000)

@eel.expose
def translate(input_text, src_lang, dest_lang):
    googletrans_api.translate(input_text, src_lang, dest_lang)
    
desktop.start(app_name, end_point, size)