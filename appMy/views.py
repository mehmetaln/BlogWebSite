from django.shortcuts import *
from appMy.models import *
from django.db.models import Count
from django.db.models import Q
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages # kullanıc

# Create your views here.


def indexPage(request):
    blog_list = Blog.objects.all()
    blog_random_list = Blog.objects.all().order_by('?')
    blog_likes = Blog.objects.annotate(q_count = Count('likes')).order_by("-q_count")
    blog_comments = Blog.objects.all().order_by('-comment_num')
    context = {
        "blog_list":blog_list,
        "blog_random_list": blog_random_list,
        "blog_comments": blog_comments[:4],
        "blog_likes":blog_likes[:5]
        
    }
    return render(request, "index.html", context)
def detailPage(request,bid):
    blog= Blog.objects.get(id=bid)
    comment_list = Comment.objects.filter(blog=blog)
    
    
    if request.method == "POST":
      text = request.POST.get("text")
      # request.user => girişli kullanıcı
      comment = Comment(text=text, blog=blog, user=request.user)
      comment.save()
      
      blog.comment_num += 1
      blog.save()
    
    
    context = {
        "blog":blog,
        "comment_list":comment_list,
        "blog_random_list" : Blog.objects.all().order_by('?'),
        "blog_likes" : Blog.objects.annotate(q_count = Count('likes')).order_by("-q_count"),
        "blog_comments" : Blog.objects.all().order_by('-comment_num'),
    }
    
    return render(request, "detail.html", context)
def contactPage(request):
    
    if request.method == "POST":
        fullname = request.POST.get("fullname")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        text= request.POST.get("text")

        contact = Contact(fullname = fullname, email = email, title = subject, text = text)
        contact.save()
        
        
    context = {
        
    }
    return render(request,"contact.html",context)
def allblogPage(request, cslug=None):
    
    if cslug:
        blog_list= Blog.objects.filter(category__slug = cslug).order_by('-id')
    else:    
        blog_list = Blog.objects.all().order_by('-id')
        
    query=request.GET.get("query")
    
    if query:
        blog_list = blog_list.filter(Q(title__icontains=query) | Q(text__icontains=query))
    # else:
    #    messages.error(request, "Kullanıcı adı veya şifre yanlış!!")
    
    category_list = Category.objects.all()
    context = {
        "blog_list":blog_list,  
        "category_list":category_list
    }
    return render(request, "allblogs.html",context)
def loginPage(request):

   if request.method == "POST":
      username = request.POST.get("username")
      password = request.POST.get("password")

      user = authenticate(username=username, password=password) 
      # kontrol eder doğruysa kullanıcı adını yanlışsa None döndürür
      if user:
         login(request, user)
         
         return redirect("indexPage")
      else:
         messages.error(request, "Kullanıcı adı veya şifre yanlış!!")
         # [] messages listedir for ile döndürülmeli
   
   context = {}
   return render(request, 'user/login.html', context)
def logoutUser(request):
   logout(request)
   return redirect("loginPage")
def registerPage(request):
    if request.method =="POST":
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")
        
        boolup = boolnum = False
        boolchar =True
        
        if fname and lname and email and password1 and password2:
            #KONTROL İŞLEMLERİ
            if password1 == password2:
                nonchar = "*;:@?.,ı"
                for i in password1:
                    if i.isupper():
                        boolup = True
                    if i.isnumeric():
                        boolnum = True
                    if i in nonchar:
                        boolchar = False        
                if  boolup and boolnum and boolchar and len(password1)>6:
                    if not  User.objects.filter(username = username).exists():
                        if not User.objects.filter(email = email).exists():
                            # KAYIT İŞLEMLERİ
                            user = User.objects.create_user(first_name = fname, last_name = lname, email=email, username=username, password=password1)
                            user.save()
                            messages.success(request,"Kaydınız başarıyla tamamlandı")
                        else:
                            messages.error("Bu email başka bir kullanıcı tarafından kullanılıyor")
                    else:
                        messages.error("Bu kullanıcı adı başka bir kullanıcı tarafından kullanılıyor")
                else:
                    messages.error("Şifreniz Büyük harf, rakam içermeli ve 6 haneden büyük olmalı")
                    messages.error(f"{{nonchar}} bu karekterileri kullanmayınız parolanızda")
                    
            else:
                messages.error("Girdiğiniz şifreler eşleşmiyor")
        else:
            messages.error("Formda boş bırakılan yerler var! Lütfen doldurunuz")
    context={}
    return render(request,"user/register.html", context)