from django.urls import path
from Kościół import views
app_name = 'Cosciol'


urlpatterns = [
    path('', views.index.as_view(), name = 'index'),
    path('login/', views.logins.as_view(), name='logins'),
    path('logout/', views.logout_view.as_view(), name='logout'),
    path('contact/', views.contact_view, name='contact'),
    
    path('adminPanel/', views.PageadminPanel.as_view(), name="adminPanel"),
    path('adminPanel/form/', views.PageFormUser.as_view(), name='page_formUser'),

    path('delete/<int:pk>', views.UserDeleteView.as_view(), name='Delet_user'),
    path('delete/', views.delete_all_user.as_view(), name='delete_all_user'),
]


