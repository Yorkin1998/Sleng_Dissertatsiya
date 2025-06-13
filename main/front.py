import json
from transformers import AutoModelForSequenceClassification, AutoTokenizer
import torch
import pandas as pd
import re

uz_slang_model_name="/home/yorkin1998/Desktop/Projects/iroda/uz_slang_model/content/uz_slang_model"
# Load the trained model
model = AutoModelForSequenceClassification.from_pretrained(uz_slang_model_name)
model.eval()  # Set to evaluation mode

# Load the tokenizer
tokenizer = AutoTokenizer.from_pretrained(uz_slang_model_name)

# Move model to GPU if available
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def predict(text, word):
    input_text = f"{word} [SEP] {text}"
    tokens = tokenizer(input_text, return_tensors="pt", truncation=True, padding="max_length", max_length=256)
    tokens = {k: v.to(model.device) for k, v in tokens.items() if k != 'token_type_ids'}

    with torch.no_grad():
        logits = model(**tokens).logits
    probs = torch.softmax(logits, dim=-1)[0]
    pred = torch.argmax(probs).item()
    return {"label": pred, "confidence": float(probs[pred])}

# Excel faylni o‘qish
df = pd.read_excel('/home/yorkin1998/Desktop/Projects/Sleng_Dissertatsiya/slanglist.xlsx')
df['Sleng'] = df['Sleng'].str.lower()

# 1 so'zli va ko'p so'zli slenglarni ajratish
sleng_dict_1 = {}
sleng_list_multi = []

for i, row in df.iterrows():
    sleng = row['Sleng']
    izoh = row['Izoh']
    if len(sleng.strip().split()) == 1:
        sleng_dict_1[sleng] = izoh
    else:
        sleng_list_multi.append((sleng, izoh))

# Tokenlash
def get_tokens(text):
    return re.findall(r'\b[\w\'‘]+\b', text.lower())

# o'zak mosligi
def is_match(word, root):
    if root.endswith("moq") and len(root) > 4:
        root = root[:-3]
    return word.startswith(root)

# 1 so'zli slenglar
def find_single_word_slangs(tokens):
    results = []
    for token in tokens:
        for sleng, izoh in sleng_dict_1.items():
            if is_match(token, sleng):
                results.append((token, izoh))
    return results

# 2 yoki 3 so'zli slenglar
def find_multi_word_slangs(tokens):
    results = []
    for sleng_phrase, izoh in sleng_list_multi:
        roots = sleng_phrase.split()
        if len(roots) > len(tokens):
            continue
        for i in range(len(tokens) - len(roots) + 1):
            match = True
            for j, root in enumerate(roots):
                if not is_match(tokens[i + j], root):
                    match = False
                    break
            if match:
                matched_phrase = " ".join(tokens[i:i+len(roots)])
                results.append((matched_phrase, izoh))
    return results

# Umumiy funksiya
def find_all_slangs(text):
    tokens = get_tokens(text)
    found = find_single_word_slangs(tokens)
    found += find_multi_word_slangs(tokens)
    return found

# matn = "Tg'ri ilon sichqon suvarak chayon kaltakesak deb manam eshitganman"  # Bu yerga xohlagan matningizni yozing
# natijalar = find_all_slangs(matn)

# if natijalar:
#     is_slang = False
#     slang_word = ""
#     slang_meaning = ""
#     for soz, izoh in natijalar:
#         result = predict(matn, soz)
#         if result["label"] == 1:
#             is_slang = True
#             slang_word = soz
#             slang_meaning = izoh
#             break  # Birinchi haqiqiy sleng topilishi bilan to‘xtaydi

#     if is_slang:
#         print("🟡 BU SLENGLIK GAP!")
#         print(f"🔸 Sleng so‘z: {slang_word}")
#         print(f"🔍 Izoh: {slang_meaning}")
#     else:
#         print("🟢 Bu oddiy gap (sleng topildi, lekin model uni slang deb belgilamadi).")
# else:
#     print("🟢 Bu oddiy gap (sleng topilmadi).")

# Matn kiritish
# matn = 'Darsda ustoz o‘quvchini shunaqa gap bilan chizib ketdi – hamma jim bo‘ldi.'
# matn = "buxanka bosh bo'ganakansizde oka"
# natijalar = find_all_slangs(matn)

# Natijalarni chiqarish
# if natijalar:
#     print(natijalar)
#   # agar so'z faqat slang bo'lsa, unda slang deb chiqar
#   # aks holda
#   #  result=predict(matn, natijalar[0].soz)
#   #
#     print("\nTopilgan slenglar:")
#     for soz, izoh in natijalar:
#         print(f"{soz} → {izoh}")
# else:
#     print("Hech qanday sleng topilmadi.")
# if natijalar:
#     print("\nTopilgan slenglar:")
#     for soz, izoh in natijalar:
#         result = predict(matn, soz)
#         label = "Sleng" if result["label"] == 1 else "Oddiy"
#         confidence = f"{result['confidence']*100:.2f}%"
#         print(f"{soz} → {izoh} | Bashorat: {label} (Ishonchlilik: {confidence})")
# else:
#     print("Hech qanday sleng topilmadi.")
