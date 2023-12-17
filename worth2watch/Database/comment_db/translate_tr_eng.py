from googletrans import Translator

def translate_text(text, source_language='tr', target_language='en'):
    translator = Translator()
    result = translator.translate(text, src=source_language, dest=target_language)
    return result.text