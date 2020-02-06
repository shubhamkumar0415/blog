from django.shortcuts import render
from .models import Post

posts =[
    {
        'author':'Shubham',
        'title':'Blog Post 1',
        'content':'First post content',
        'date_posted':'aug 2,2020'
    },
{
        'author':'Ram',
        'title':'Blog Post 2',
        'content':'Second post content',
        'date_posted':'aug 4,2020'
    }

]

# Create your views here.
def home(request):
    context = {
        'posts':Post.objects.all()

    }
    return render(request,'blog/home.html',context)

def about(request):
    return render(request,'blog/about.html',{'title':'about'})
