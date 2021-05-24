from googletrans import Translator
import eel

def translate(input_text, src_lang, dest_lang):
    translator = Translator()
    translated = translator.translate(input_text, src=src_lang, dest=dest_lang)
    eel.view_log_js(f'翻訳前：『{input_text}』')
    eel.view_log_js(f'翻訳後：『{translated.text}』\n')