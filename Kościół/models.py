from django.db import models

# Create your models here.
class TextUpdate(models.Model):
    # Окно описания
    title_bible = models.TextField(verbose_name="Заголовок", default="Заголовок", blank=True)
    text_bible = models.TextField(verbose_name="Текст", default="Текст", blank=True)
    
    # Окно адрес
    text_adres = models.CharField(max_length=50, verbose_name="Адрес", default="Адрес", blank=True)
    text_adres_link = models.CharField(max_length=200,verbose_name="Адрес_ccилка", default="Адрес_ccилка", blank=True)
    phone = models.CharField(max_length=20, verbose_name="Телефон", default="+000000000", blank=True) 

    # О нас
    about_us_text1 = models.TextField(verbose_name="Первый абзац", default="Текст", blank=True)
    about_us_text2 = models.TextField(verbose_name="Второй абзац", default="Текст", blank=True)
    
    # Окно Email
    text_email = models.EmailField(default="example@email.com", blank=True)

    # Окно meting schedule 
    meting_saturday = models.CharField(max_length=50, verbose_name="Суббота", default="10:00", blank=True)
    meting_sanday = models.CharField(max_length=50, verbose_name="Воскресенье", default="10:00", blank=True)

    is_reg_open = models.BooleanField(default=False, verbose_name="Регестрация открыта")
    text_register = models.TextField(verbose_name="Текст для регистрации",blank=True)
    def __str__(self):
        return "Настройки Контента Главной"