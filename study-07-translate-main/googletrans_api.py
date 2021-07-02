from googletrans import Translator
import datetime
import eel

def translate(input_text, src_lang, dest_lang):
    translator = Translator()
    translated = translator.translate(input_text, src=src_lang, dest=dest_lang)
    now = datetime.datetime.now().strftime('%Y/%m/%d %H:%M:%S')
    eel.view_log_js(f'{translated.text}\n')