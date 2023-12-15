from django.shortcuts import render
from appMy.models import Blog
# Create your views here.


def indexPage(request):
    blog_list = Blog.objects.all()
    blog_random_list = Blog.objects.all().order_by('?')
    context = {
        "blog_list":blog_list,
        "blog_random_list": blog_random_list[:4]
    }
    return render(request, "index.html", context)



def detailPage(request,bid):
    blog= Blog.objects.get(id=bid)
    
    
    
    
    context = {
        "blog":blog,
    }
    return render(request, "detail.html", context)