from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import TextUpdate

#Здесь мы решаем, какие именно поля из базы можно трогать админу. Это "фильтр".
class UpdateForm(forms.ModelForm):
    class Meta:
        model = TextUpdate
        fields = ['title_bible', 'text_bible', 'text_adres', 'about_us_text1', 'about_us_text2', 'text_email', 'meting_saturday', 'meting_sanday', 'phone', 'text_adres_link']# какие поля по name  будем принимать из html а так же с какими полями работать из баз даных

class UserCreateForm(UserCreationForm):

    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'reg-inpt',
            'placeholder': 'Введите email'
        }))
    
    username = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'reg-inpt',
            'placeholder': 'Введите имя'
        })
    )

    password1 = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'reg-inpt',
            'placeholder': 'Придумайте пароль'
        })
    )
    
    password2 = forms.CharField(
        label='Повторите пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'reg-inpt',
            'placeholder': 'Повторите пароль'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    # Можно и без нее но тут мы проверяем на то что бы небыло несколько аков на эту почту
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Этот адрес электронной почты уже используется.')
        return email