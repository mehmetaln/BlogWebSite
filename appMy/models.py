from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, related_name = "user1", verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    title = models.CharField(("Başlık"), max_length=50)
    text= models.TextField(("Blog Yazısı"))    
    image = models.ImageField(("Resim"), upload_to="blog",)
    date_now = models.DateTimeField(("Tarih - Saat"), auto_now_add=False)
    
    
    def __str__(self):
        return self.title