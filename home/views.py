from typing import Any
from django import http
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseBase
from django.shortcuts import render, redirect, get_object_or_404
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views import View
from django.views.generic.base import TemplateView

from .forms import PostCreateUpdateForm,CommentCreateForm,CommentReplyForm,PostSearchForm

from .models import Post, Comment, Vote


class HomeView(View):
    form_class=PostSearchForm
    def get(self,request):
        posts=Post.objects.all()
        if request.GET.get('search'):
            posts=posts.filter(body__icontains=request.GET['search'])
        return  render(request,'home/index.html',{'posts':posts,'form':self.form_class})


class PostDetailView(View):
    form_class=CommentCreateForm
    form_class_reply=CommentReplyForm
    def get(self,request,post_id,post_slug):
        post=get_object_or_404(Post,slug=post_slug,id=post_id)
        comments=post.pcomments.filter(is_reply=False)
        can_like=False
        if request.user.is_authenticated and post.user_can_like(request.user):
            can_like=True
        return render(request,'home/detail.html',{'reply_form':self.form_class_reply,
                                                  'form':self.form_class,'post':post,'comments':comments,'can_like':can_like})
    @method_decorator(login_required)
    def post(self,request,post_id,post_slug):
        form=self.form_class(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)
            new_comment.uer=request.user
            new_comment.post=get_object_or_404(Post,id=post_id)
            new_comment.save()
            messages.success(request,'comment saved successfully','success')
            return redirect('home:post_detail',post_id,post_slug)

class PostDeleteView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post=get_object_or_404(Post,id=post_id)
        if post.user.id == request.user.id:
            post.delete()
            messages.success(request,'post deleted successfully','success')
        else:
            messages.error(request,'this post does not belong to you','warning')
        return redirect('home:home')

class PostUpdateView(LoginRequiredMixin,View):
    def dispatch(self, request: http.HttpRequest, *args: Any, **kwargs: Any) -> HttpResponseBase:
        post = get_object_or_404(Post,id=kwargs['post_id'])
        if post.user.id != request.user.id:
            messages.error(request, 'this is not your post', 'danger')
            return redirect('home:home')
        return super().dispatch(request,*args,**kwargs)
    def get(self,request,post_id):
        post=get_object_or_404(Post,id=post_id)
        if post.user.id != request.user.id:
            messages.error(request,'this is not your post','warning')
            return redirect('home:home')
        form=PostCreateUpdateForm(instance=post)
        return render(request,'home/update.html',{'form':form})
    def post(self,request,post_id):
            post=get_object_or_404(Post,pk=post_id)
            form=PostCreateUpdateForm(request.POST,instance=post)
            if form.is_valid():
                new=form.save(commit=False)
                new.slug=slugify(form.cleaned_data['body'][:30])
                new.save()
                messages.success(request,'post update successfully','success')
                return redirect('home:post_detail',post_id,post_slug)
            return render(request,'home/update.html',{'form':form})
class PostCreateView(LoginRequiredMixin,View):
    def get(self,request,*args,**kwargs):
        form=PostCreateUpdateForm
        return render(request,'home/create.html',{'form':form})
    def post(self,request,*args,**kwargs):
        form=PostCreateUpdateForm(request.POST)
        if form.is_valid():
            new=form.save(commit=False)
            new.slug=slugify(form.cleaned_data['body'][:30])
            new.user=request.user
            new.save()
            messages.success(request,'post created successfully','success')
            return redirect('home:post_detail',post.id,post.user)
        return render(request,'home/create.html')

class PostAddReplyView(LoginRequiredMixin,View):
        form_class=CommentReplyForm
        def post(self,request,post_id,comment_id):
            post=get_object_or_404(Post,id=post_id)
            comment=get_object_or_404(Comment,id=comment_id)
            form=self.form_class(request.POST)
            if form.is_valid():
                reply=form.save(commit=False)
                reply.user=request.user
                reply.post=post
                reply.reply=comment
                reply.is_reply=True
                reply.save()
                messages.success(request,'reply submitted successfully','success')
            return redirect('home:post_detail',post.id,post.slug)

class PostLikeView(LoginRequiredMixin,View):
    def get(self,request,post_id):
        post=get_object_or_404(Post,id=post_id)
        like=Vote.objects.filter(post=post,user=request.user)
        if like.exists():
            Vote.objects.create(post=post,user=request.user)
            messages.error(request,'you have already liked','warning')
        else:
            messages.success(request,'you liked this post','success')
        return redirect('home:post_detail',post.id,post.slug)
