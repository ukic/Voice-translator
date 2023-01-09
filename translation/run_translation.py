from easynmt import EasyNMT


# from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
# en_pl_tokenizer = AutoTokenizer.from_pretrained("Helsinki-NLP/opus-mt-pl-en")
# en_pl_model = AutoModelForSeq2SeqLM.from_pretrained("Helsinki-NLP/opus-mt-pl-en")
#
# text = "Jak się masz?"
# encoded_input = en_pl_tokenizer(text, return_tensors="pt")
# output = en_pl_model.generate(**encoded_input)
# out_text = en_pl_tokenizer.batch_decode(output, bskip_special_tokens=True)
# print(out_text)

# import server
# import json
# import numpy as np
#
# with open('services.json', 'r') as configfile:
#     service = json.load(configfile)
#
# model = np.load(".\models\en-pl\opus.bpe32k-bpe32k.transformer.model1.npz.best-perplexity.npz")
# translator = server.TranslatorInterface("en", "pl", service, model)
#
# a = translator.translate("That is very satisfying"")
# print(a)

def translate_easy(target_lang=str, source_lang=str, text=str) -> str:

    if target_lang == "pl" and source_lang == "en":
        model = EasyNMT('m2m_100_418M')
    else:
        model = EasyNMT('opus-mt')
    translated = model.translate(text, target_lang, source_lang)
    return translated
