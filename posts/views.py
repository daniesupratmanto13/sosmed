from django.urls import reverse_lazy
from django.contrib import messages
from django.shortcuts import redirect, render
from django.http.response import JsonResponse
from django.views.generic import UpdateView, DeleteView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import *
from .forms import *
from profiles.models import Profile


@login_required
def postCommentAndListView(request):
    posts = Post.objects.all()
    profile = Profile.objects.get(user=request.user)

    post_form = PostForm()
    comment_form = CommentForm()
    post_added = False

    if request.method == 'POST':

        if 'submit_post' in request.POST:
            post_form = PostForm(request.POST, request.FILES or None)
            if post_form.is_valid():
                instance = post_form.save(commit=False)
                instance.author = profile
                instance.save()
                post_form = PostForm()
                post_added = True

        if 'sumbit_comment' in request.POST:
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                instance = comment_form.save(commit=False)
                instance.user = profile
                instance.post = Post.objects.get(
                    id=request.POST.get('post_id'))
                instance.save()
                comment_form = CommentForm()

    context = {
        'posts': posts,
        'profile': profile,
        'post_form': post_form,
        'comment_form': comment_form,
        'post_added': post_added,
    }

    return render(request, 'posts/index_posts.html', context)


@login_required
def likeUnlikePostView(request):
    user = request.user

    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = Post.objects.get(id=post_id)
        profile = Profile.objects.get(user=user)

        if profile in post.liked.all():
            post.liked.remove(profile)
        else:
            post.liked.add(profile)

        like, created = Like.objects.get_or_create(user=profile, post=post)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'

        like.save()
        post.save()

        data = {
            'value': like.value,
            'likes': post.likeCount,
        }

        return JsonResponse(data, safe=True)

    return redirect('posts:index')


class DeletePostView(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'posts/confirm_del_post.html'
    success_url = reverse_lazy('posts:index')
    context_object_name = 'post'

    def get_object(self, *args, **kwargs):
        pk = self.kwargs.get('pk')
        post = Post.objects.get(pk=pk)
        if not self.request.user == post.author.user:
            messages.warning(self.request, 'You not the author')
        return post


class UpdatePostView(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostForm
    template_name = 'posts/update_post.html'
    success_url = reverse_lazy('posts:index')

    def form_valid(self, form):
        profile = Profile.objects.get(user=self.request.user)
        if form.instance.author == profile:
            return super().form_valid(form)
        else:
            form.add_error(None, 'You not the author')
            return super().form_invalid(form)
