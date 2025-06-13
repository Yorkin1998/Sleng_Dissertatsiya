from django.shortcuts import render
from django.core.cache import cache

from .models import (SlangModel, )
# Create your views here.
def index(request):
    slangs = cache.get('slangs')
    if not slangs:
        slangs = SlangModel.objects.all()
        cache.set('slangs', slangs, timeout = 150)
    
    return render(request=request, template_name='index.html', context={
        'slangs': slangs
    })