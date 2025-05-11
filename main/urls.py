from django.urls import path
from .views import index
from .updation import check_slang

urlpatterns = [

    path('', index, name="index"),
    path('check/', check_slang, name='check_slang'),

]
