from django.urls import path
from Kościół import views
app_name = 'Cosciol'


urlpatterns = [
    path('', views.index, name = 'index'),
    path('register/', views.register, name = 'register'),
    
]
