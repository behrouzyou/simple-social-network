
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponseBase
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View

from home.models import Post
from .forms import *
from django.contrib.auth.models import User
from django.contrib import messages

from .models import Relation


class UserRegisterView(View):

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)
    def get(self,request):
        form=UserRegisterForm()
        return render(request,'account/register.html',{'form':form})
    def post(self,request):
        form=UserRegisterForm(request.POST)
        if form.is_valid():
            User.objects.create(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],password=form.cleaned_data['password'])
            messages.success(request,'you are registered successfully','success')
            return redirect('home:home')
        return render(request,'account/register.html',{'form':form})

class UserLoginView(View):
    def setup(self, request: HttpRequest, *args: Any, **kwargs: Any) -> None:
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)
    form_class=UserLoginForm
    def get(self,request):
        form=self.form_class()
        return render(request,'account/login.html',{'form':form})
    def post(self,request):
        form=self.form_class(request.POST)
        if form.is_valid():
            user=authenticate(request,username=form.cleaned_data['username'],password=form.cleaned_data['password1'])
            if user is not None:
                login(request,user)
                messages.success(request,'you are logged in','success')
                if self.next:
                    return redirect(self.next)
                return redirect('home:home')
            messages.error(request,'username or password is wrong','warning')
        return render(request,'account/login.html',{'form':form})

class UserLogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'you logged out successfully','success')
        return redirect('home:home')

class UserProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        is_following=False
        user=get_object_or_404(User,id=user_id)
        posts =Post.objects.filter(user =user)
        relation= Relation.objects.filter(from_user=request.user,to_user=user)
        if relation.exists():
            is_following =True
        return render(request,'account/profile.html',{'user':user,'posts':posts,'is_following':is_following})
class UserFollowView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=get_object_or_404(User,id=user_id)
        relation=Relation.objects.filter(from_user=request.user,to_user=user).exists()
        if relation:
            messages.error(request,f'you already following {user.username}','warning')
        else:
            Relation.objects.create(from_user=request.user,to_user=user)
            messages.success(request,f'you are start following {user.username}','success')
        return redirect('account:user_profile',user.id)
class UserUnfollowView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user=get_object_or_404(User,id=user_id)
        relation=Relation.objects.filter(from_user=request.user,to_user=user)
        if not relation.exists():
            messages.error(request,f'you are not following {user.username}','warning')
        else:
            relation.delete()
            messages.success(request,f'you stop following {user.username}','success')
        return redirect('account:user_profile',user.id)

class EditUserView(LoginRequiredMixin,View):
    form_class=EditUserForm
    def get(self,request):
        form=self.form_class(instance=request.user.profile,initial={'email':request.user.email})
        return render(request,'account/edit_profile.html',{'form':form})
    def post(self,request):
        form=self.form_class(request.POST,instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email=form.cleaned_data['email']
            request.user.save()
            messages.success(request,'profile edited successfully','success')
        return redirect('account:user_profile',request.user.id)