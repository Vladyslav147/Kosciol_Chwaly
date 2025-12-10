from django.urls import path
from Kościół import views
app_name = 'Cosciol'


urlpatterns = [
    path('', views.index, name = 'index'),
    # path('register/', views.register, name = 'register'),
    path('login/', views.logins, name='logins'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact_view, name='contact'),
    path('adminPanel/', views.adminPanel, name="adminPanel"),
]
