from django.db import models

# Create your models here.
class GalleryPost(models.Model):
    title = models.CharField('Название', max_length=100)
    date = models.DateField('Дата события')
    description = models.TextField('Описание')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.date})"
    
    class Meta:
        verbose_name = 'Пост галереи'
        verbose_name_plural = 'Посты галереи'
        ordering = ['-date']
    
class GalleryImage(models.Model):
    post = models.ForeignKey(GalleryPost, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='gallery_photos/')
    
    def __str__(self):
        return f"Фото для {self.post.title}"