from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Blog(models.Model):
    user = models.ForeignKey(User, related_name = "user1", verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    title = models.CharField(("Başlık"), max_length=50)
    text= models.TextField(("Blog Yazısı"))    
    image = models.ImageField(("Resim"), upload_to="blog",)
    date_now = models.DateTimeField(("Tarih - Saat"), auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="user2", verbose_name=("Begenen Kullanıcılar"),blank=True)
    comment_num = models.IntegerField(("Yorum Sayisi"), default=0)
    
    def __str__(self):
        return self.title



class Comment(models.Model):
    user= models.ForeignKey(User, verbose_name=("Kullanıcı"), on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, verbose_name=("Yorum Yapılan Blog"), on_delete=models.CASCADE)
    text = models.TextField(("Yorum"))
    date_now = models.DateTimeField(("Tarih - Saat"), auto_now_add=True)
    
    def __str__(self):
        return self.blog.title