from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegisterForm
# Create your views here.
class Home(View):
    def get(self,request,*args,**kwargs):
        return render(request,'landing/index.html')


class UserRegister(View):
    def get(self,request,*args,**kwargs):
        form = UserRegisterForm()
        context = {'form':form}
        return render(request,'landing/register.html',context)

    def post(self,request,*args,**kwargs):
        form = UserRegisterForm(request.POST)
        if request.method == "POST":
            form = UserRegisterForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('login')
            else:
                msg = "Do Not validate"
        context = {'msg':msg,'form':form}
        return render(request,'landing/register.html',context)

class Login(View):
    def get(self,request,*args,**kwargs):
        return render(request,'landing/login.html')