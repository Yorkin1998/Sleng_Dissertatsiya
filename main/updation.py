from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .front import find_all_slangs, predict
import json

@csrf_exempt
def check_slang(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        text = data.get("text")

        if not text:
            return JsonResponse({"error": "Matn yuborilmadi."}, status=400)

        results = find_all_slangs(text)

        response = []
        for word, meaning in results:
            prediction = predict(text, word)
            label = "Sleng" if prediction['label'] == 1 else "Oddiy"
            confidence = f"{prediction['confidence'] * 100:.2f}%"
            response.append({
                "word": word,
                "meaning": meaning,
                "label": label,
                "confidence": confidence
            })

        return JsonResponse({"results": response})