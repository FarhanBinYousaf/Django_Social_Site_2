from django.shortcuts import render,redirect
from django.views import View
from .models import Post,Comment,UserProfile
from .forms import PostsForm, CommentForm
from django.views.generic.edit import UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
# Create your views here.

class PostListView(View):
    def get(self,request,*args,**kwargs):
        logged_in_user = request.user
        posts = Post.objects.filter(
            author__profile__followers__in=[logged_in_user.id]
            ).order_by('-created_on')
        form = PostsForm()
        context = {'posts':posts,'form':form}
        return render(request,'social/post_list.html',context)
    def post(self,request,*args,**kwargs):
        posts = Post.objects.all().order_by('-created_on')
        form = PostsForm(request.POST)

        if form.is_valid():
            post_form = form.save(commit=False)
            post_form.author = request.user
            post_form.save()
        context = {'posts':posts,'form':form}
        return render(request,'social/post_list.html',context)


class PostDetailView(View):
    def get(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        commentForm = CommentForm()
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        context = {'post':post,'commentForm':commentForm,'comments':comments}
        return render(request,'social/post_detail.html',context)

    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)
        commentForm = CommentForm(request.POST)
        if commentForm.is_valid():
            new_comment = commentForm.save(commit=False)
            new_comment.author = request.user
            new_comment.post = post
            new_comment.save()
        comments = Comment.objects.filter(post=post).order_by('-created_on')
        context = {'post':post,'commentForm':commentForm,'comments':comments}
        return render(request,'social/post_detail.html',context)
class EditPostView(LoginRequiredMixin,UserPassesTestMixin,UpdateView):
    model = Post
    fields = ['body']
    template_name = 'social/edit_post.html'


    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('post',kwargs={'pk':pk})

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author

class DeletePostView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'social/delete_post.html'
    success_url = reverse_lazy('post_list')

    def test_func(self):
        post = self.get_object()
        return self.request.user == post.author


class CommentDeleteView(LoginRequiredMixin,UserPassesTestMixin, DeleteView):
    model = Comment
    template_name = 'social/comment_delete.html'

    def get_success_url(self):
        pk = self.kwargs['post_pk']
        return reverse_lazy('post',kwargs={'pk':pk})

    def test_func(self):
        comment = self.get_object()
        return self.request.user == comment.author

class UserProfileView(LoginRequiredMixin,View):
    login_url = '/login/'
    redirect_field_name = 'login'
    def get(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        user = profile.user
        posts = Post.objects.filter(author=user).order_by('-created_on')

        followers = profile.followers.all()
        if len(followers) == 0:
            followed = False

        for follower in followers:
            if follower == request.user:
                followed = True
                break
            else:
                followed = False

        number_of_followers = len(followers)
        context = {'profile':profile,'posts':posts,'user':user,'number_of_followers':number_of_followers,'followed':followed}
        return render(request,'social/user_profile.html',context)



class UpdateProfileView(LoginRequiredMixin,UserPassesTestMixin, UpdateView):
    model = UserProfile
    fields = ['name','bio','birth_date','location','image']
    template_name = 'social/profile_edit.html'

    def get_success_url(self):
        pk = self.kwargs['pk']
        return reverse_lazy('user-profile',kwargs={'pk':pk})

    def test_func(self):
        profile = self.get_object()
        return self.request.user == profile.user



class ProfileSearch(View):
    def get(self,request,*args,**kwargs):
        query = self.request.GET.get('query')
        profile_list = UserProfile.objects.filter(
            Q(user__username__icontains=query)
            )
        
        context = {'profile_list':profile_list}
        return render(request,'social/profile_search.html',context)


class AddLike(LoginRequiredMixin, View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)

        disliked = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                disliked = True
                break
        if disliked:
            post.dislikes.remove(request.user)
        liked = False
        for like in post.likes.all():
            if like == request.user:
                liked = True
                break

        if not liked:
            post.likes.add(request.user)
        if liked:
            post.likes.remove(request.user)
        next = request.POST.get('next', '/')
        return HttpResponseRedirect(next)

class AddDisLike(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        post = Post.objects.get(pk=pk)

        liked = False
        for like in post.likes.all():
            if like == request.user:
                liked = True
                break
        if liked:
            post.likes.remove(request.user)

        disliked = False
        for dislike in post.dislikes.all():
            if dislike == request.user:
                disliked = True
                break
        if not disliked:
            post.dislikes.add(request.user)
        if disliked:
            post.dislikes.remove(request.user)

        next = request.POST.get('next','/')
        return HttpResponseRedirect(next)

class AddFollower(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.add(request.user)

        return redirect('user-profile',pk=profile.pk)


class RemoveFollower(LoginRequiredMixin,View):
    def post(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        profile.followers.remove(request.user)

        return redirect('user-profile',pk=profile.pk)

class FollowersList(View):
    def get(self,request,pk,*args,**kwargs):
        profile = UserProfile.objects.get(pk=pk)
        followers = profile.followers.all()

        context = {'profile':profile,'followers':followers}
        return render(request,'social/followers_list.html',context)

