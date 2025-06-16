from django.urls import path
from .views import index
from .updation import check_slang, load_more_slangs

urlpatterns = [

    path('', index, name="index"),
    path('check/', check_slang, name='check_slang'),
    path('ajax/load-slangs/', load_more_slangs, name='load_more_slangs'),
]
