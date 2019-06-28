from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.core.paginator import Paginator
from .models import Blog

from django.contrib.auth.models import User
from django.contrib import auth


def home(request):
    blogs = Blog.objects #쿼리셋
    #블로그의 모든 글을 대상으로
    blog_list = Blog.objects.all()
    #블로그 객체 3개를 한 페이지로 자르기
    paginator = Paginator(blog_list, 3)
    #request된 페이지가 뭔지 알아내고(request페이지를 변수에 담아내고)
    page = request.GET.get('page')
    #request된 페이지가 얻어온 뒤 return 해준다.
    posts = paginator.get_page(page)
    return render(request, 'home.html', {'blogs' : blogs, 'posts' : posts})





def detail(request, blog_id):
    details = get_object_or_404(Blog, pk=blog_id) #pk는 검색조건
    return render(request, 'detail.html', {'details':details})

def new(request):
    return render(request, 'new.html')

def create(request):#입력받은 내용을 DB에 넣어주는 함수
    blog = Blog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.datetime.now()
    blog.save() #DB에 저장해라 / 객체.delete()는 지우라는 의미를 갖는다.
    return redirect('/blog/'+str(blog.id)) #url은 항상 문자형이라 str 처리해준다.
 
def portfolio(request):
    return render(request, 'portfolio.html')

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password) #실제로 저장된 회원이 맞는지 확인하는 함수
        if user is not None:
            auth.login(request, user)
            return redirect('home') #로그인 성공시 홈으로 이동
        else:
            return render(request, 'home.html', {'error':'username or password is incorrect.'})
    else:
        return render(request, 'home.html')




