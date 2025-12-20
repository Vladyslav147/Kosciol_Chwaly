from django.urls import path
from Kościół import views
app_name = 'Cosciol'


urlpatterns = [
    path('', views.index, name = 'index'),
    path('login/', views.logins, name='logins'),
    path('logout/', views.logout_view, name='logout'),
    path('contact/', views.contact_view, name='contact'),
    
    path('adminPanel/', views.PageadminPanel, name="adminPanel"),
    path('adminPanel/form/', views.PageformUsers, name='page_formUser'),

    path('delete/<int:id>', views.user_delete, name='Delet_user'),
    path('delete/', views.delete_all_user, name='delete_all_user'),
]


