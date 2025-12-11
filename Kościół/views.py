import os
from dotenv import load_dotenv
import requests # для выхода в интернет
from django.shortcuts import render
from .forms import UserCreateForm
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404 
from django.contrib import messages
from django.contrib.auth.decorators import login_required
load_dotenv()

from .models import TextUpdate
from .forms import UpdateForm
TG_TOKEN = os.getenv('TG_TOKEN')
TG_CHAT_ID = os.getenv('TG_CHAT_ID')




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


def index(request):
    # 1. Достаем ту же самую запись, что правим в админке (id=1)
    # Используем get_or_create, чтобы сайт не сломался, если запись удалят
    church_info, created = TextUpdate.objects.get_or_create(id=1)

    # 2. Создаем контекст
    context = {
        'info': church_info  # Мы назвали переменную 'info'
    }

    # 3. Передаем контекст в рендер
    return render(request, 'main/index.html', context)

def logins(request):
    if request.method == 'POST':
        # 1. Получаем данные
        username_data = request.POST.get('username') #Ложым данные зи сайта в переменные 
        password_data = request.POST.get('password')
        # 2. Проверяем логин и пароль
        user = authenticate(request, username=username_data, password=password_data) #Тут проверка на то что если ли такой админ в баз дане делает это authenticate

        if user is not None:#если ты не пустой то проходим дальше если пустой тоесть ты None то проверка не будет пройдена 
            if user.is_staff:  # Проверяем, является ли он Персоналом (Админом)
                # Если Админ — пускаем
                login(request, user)
                return redirect('Cosciol:index') 
            else:
                # Если пароль верный, но он ОБЫЧНЫЙ юзер — не пускаем
                messages.error(request, 'Доступ разрешен только администраторам')
        else:
            # 4. Если пароль вообще неверный
            messages.error(request, 'Неверное имя пользователя или пароль')
    return render(request, 'registers/login.html')


def logout_view(request):
    logout(request)
    return redirect('Cosciol:index')

@login_required
def adminPanel(request):
    obj, create = TextUpdate.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = UpdateForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('Cosciol:index')
    else:
        form = UpdateForm(instance=obj)

    context = {
        'form': form
    }
    return render(request, 'registers/adminPanel.html', context)



"""
def register(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('Cosciol:index')
    else:
        # Если это GET-запрос (просто зашли на страницу), создаем пустую форму
        form = UserCreateForm()
    return render(request, 'registers/register.html', {'form': form})

"""