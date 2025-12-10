from django.db import models

# Create your models here.
class TextUpdate(models.Model):
    # Используем verbose_name, чтобы в админке было понятно, что это за поле
    text_bible = models.TextField(verbose_name="Цитата из Библии")
    text_about = models.TextField(verbose_name="Текст О нас")
    
    # Исправил опечатку fotur -> footer
    text_footer = models.CharField(max_length=200, verbose_name="Текст в футере") 
    
    # ВАЖНО: CharField для телефона!
    phone = models.CharField(max_length=20, verbose_name="Телефон") 
    
    date_saturday = models.CharField(max_length=50, verbose_name="Время Суббота")
    date_sunday = models.CharField(max_length=50, verbose_name="Время Воскресенье")

    # Чтобы в админке красиво называлось
    def __str__(self):
        return "Настройки Контента Главной"