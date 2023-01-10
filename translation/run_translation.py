from easynmt import EasyNMT

def translate_easy(target_lang=str, source_lang=str, text=str) -> str:

    if target_lang == "pl" and source_lang == "en":
        model = EasyNMT('m2m_100_418M')
    else:
        model = EasyNMT('opus-mt')
    translated = model.translate(text, target_lang, source_lang)
    return translated

