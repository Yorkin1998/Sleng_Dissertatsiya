
from django.core.paginator import Paginator
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

import json

from .front import find_all_slangs, predict
from .models import SlangSentence

@csrf_exempt
def check_slang(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get("text")

        if not text:
            return JsonResponse({"error": "Matn yuborilmadi."}, status=400)

        results = find_all_slangs(text)
        response = []
        is_slang = False  # umumiy holat

        for word, meaning in results:
            prediction = predict(text, word)
            label = "Sleng" if prediction['label'] == 1 else "Oddiy"
            confidence = f"{prediction['confidence'] * 100:.2f}%"
            
            if prediction['label'] == 1:
                is_slang = True

            # Sleng so'z va izohni responsega qo'shamiz
            response.append({
                "word": word,
                "meaning": meaning,
                "label": label,
                "confidence": confidence
            })

        return JsonResponse({
            "slang": is_slang,  # Slenglik gapni tekshirish
            "results": response  # Sleng va izohlar bilan natijani qaytarish
        })

    return JsonResponse({"error": "Faqat POST so‘rovlari qabul qilinadi."}, status=405)

@require_GET
def load_more_slangs(request):
    page = int(request.GET.get("page", 1))
    slangs = SlangSentence.objects.filter().order_by('?')
    paginator = Paginator(slangs, 5)  # Har safar 5 tadan

    try:
        slang_page = paginator.page(page)
    except:
        return JsonResponse({'data': [], 'has_next': False})

    data = [
        {
            'slang': s.slang,
            'slang_word': s.slang_word 
        } for s in slang_page
    ]

    return JsonResponse({
        'data': data,
        'has_next': slang_page.has_next()
    })