import os
from django.contrib import messages
from dotenv import load_dotenv
import requests # для выхода в интернет
from django.shortcuts import render
from .forms import UserCreateForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
load_dotenv()

# для CBV
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.views.generic.edit import DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import CreateView
from django.contrib.auth.views import LoginView, LogoutView

from .models import TextUpdate, UserRegistration
from .forms import UserRegistrationForm
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')


# Вызов отправки данных на телеграм 
def send_telegram(message):
    url = f"https://api.telegram.org/bot{TG_TOKEN}/sendMessage"
    # 2. КОРОБКА (Payload): Собираем данные для Телеграма в словарь.
    payload = {
        'chat_id': TG_CHAT_ID,  # Куда доставить (Твой личный ID)
        'text': message,        # Что доставить (Текст заявки)
        'parse_mode': 'HTML'    # Инструкция: "Понимай теги <b> как жирный шрифт"
    }
    try:
        requests.post(url, data=payload)
    except Exception as error:
        print(f'Ошибка отправки в ТГ: {error}')
def contact_view(request):
    if request.method == 'POST': 
        name = request.POST.get('name')
        Email = request.POST.get('Email')
        Temat = request.POST.get('Temat')
        messagess = request.POST.get('messages')

        # 2. Пакуем то что достали в красивый текст как будет отправлено в тг 
        full_message = (
            f"<b>Новая заявка</b>\n\n"
            f"<b>Имя:</b> {name}\n"
            f"<b>Email:</b> {Email}\n"
            f"<b>Тема:</b> {Temat}\n"
            f"<b>Сообщение:</b> {messagess}\n"
        )

        # 4. ВЫЗОВ КУРЬЕРА: Отдаем готовый текст функции отправки
        send_telegram(full_message)

        messages.success(request, 'Сообщение успешно отправлено!')
        return redirect('Cosciol:index')
    
    # Если это не POST запрос, просто кидаем на главную
    return redirect('Cosciol:index')

# Вызов главной страницы
class index(CreateView):
    model = UserRegistration
    form_class = UserRegistrationForm
    template_name = 'main/index.html'
    success_url = reverse_lazy('Cosciol:index')

    # 1. Добавляем данные info_index в контекст (аналог contex в функции)
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        info_index, create = TextUpdate.objects.get_or_create(id=1)
        context['info_index'] = info_index
        return context

    # 2. Аналог if form.is_valid(): (что делать при успехе)
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Вы успешно зарегистрированы!')
        return response

# Вызов входа админа на сайт 
class logins(LoginView):
    template_name = 'registers/login.html'
    next_page = reverse_lazy('Cosciol:index')

    def form_valid(self, form):
        user = form.get_user()

        if user.is_superuser:
            return super().form_valid(form)
        else:
            messages.error(self.request, 'Доступ разрешен только администраторам')
            return self.form_invalid(form)
        
    def form_invalid(self, form):
        messages.error(self.request, 'Неверное имя пользователя или пароль')
        return super().form_invalid(form)
    
class logout_view(LogoutView):
    next_page = reverse_lazy('Cosciol:index')

# Вызов страницы админ панели а так же всей ее логике
class PageadminPanel(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    template_name = 'registers/adminPanel.html'
    success_url = reverse_lazy('Cosciol:adminPanel')
    context_object_name = 'info'
    fields = '__all__'

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_object(self, queryset = None):
        obj, created = TextUpdate.objects.get_or_create(id=1)
        return obj
    
    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_type = request.POST.get('form_type')
        info = self.object

        if form_type == 'bible_form':
            info.title_bible = request.POST.get('title_bible')
            info.text_bible = request.POST.get('text_bible')

        elif form_type == 'adres_form':
            info.text_adres = request.POST.get('text_adres')
            info.text_adres_link = request.POST.get('text_adres_link')
            info.phone = request.POST.get('phone')
        
        elif form_type == 'about_us_form':
            info.about_us_text1 = request.POST.get('about_us_text1')
            info.about_us_text2 = request.POST.get('about_us_text2')

        elif form_type == 'Email_form':
            info.text_email = request.POST.get('text_email')
        
        elif form_type == 'meting_form':
            info.meting_saturday = request.POST.get('meting_saturday')
            info.meting_sanday = request.POST.get('meting_sanday')
        
        elif form_type == 'reg_status_form':
            info.is_reg_open = request.POST.get('is_open') == 'on'
            info.text_register = request.POST.get('text_register')
        
        info.save()
        return redirect(self.success_url)

# Вызов страницы зарегистрированных или же самой формы
class PageFormUser(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = UserRegistration
    template_name = 'registers/FormRegister.html'
    success_url = reverse_lazy('Cosciol:adminPanel')
    context_object_name = 'users'

    def test_func(self):
        return self.request.user.is_superuser
    
    def get_queryset(self):
        queryset = UserRegistration.objects.all().order_by('-created_at')
        # Получаем запрос из поиска (из URL параметров ?q=...)
        search_query = self.request.GET.get('q')

        if search_query: 
            queryset = queryset.filter(full_name__icontains=search_query)

        return queryset
    
    def get_context_data(self, **kwargs):
        # Получаем стандартный контекст (где уже лежит наш список users)
        context = super().get_context_data(**kwargs)

        # Добавляем поисковый запрос обратно в контекст (чтобы он не исчезал из поля поиска)
        context['search_query'] = self.request.GET.get('q', '')

        # Добавляем количество найденных записей
        # Мы берем его прямо из отфильтрованного списка
        context['users_integer'] = self.get_queryset().count()
        
        return context

# Вызов удаление конкретного пользователя
class UserDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = UserRegistration
    success_url = reverse_lazy('Cosciol:page_formUser')

    def test_func(self):
        return self.request.user.is_superuser

    def get(self, request, *args, **kwargs):
        return self.post(request, *args, **kwargs)

# Вызов очищение всх пользователей
class delete_all_user(LoginRequiredMixin, UserPassesTestMixin, DeleteView):

    success_url = reverse_lazy('Cosciol:page_formUser')

    def test_func(self):
        return self.request.user.is_superuser
    
    def post(self, request, *args, **kwargs):
        UserRegistration.objects.all().delete()
        return redirect(self.success_url)