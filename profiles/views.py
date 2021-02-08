from django.shortcuts import get_object_or_404, render, redirect
from django.db.models import Q
from django.views.generic import ListView, DetailView
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.
from .models import *
from .forms import *


@login_required
def myProfileView(request):

    profile = Profile.objects.get(user=request.user)
    form = ProfileForm(request.POST or None,
                       request.FILES or None, instance=profile)
    confirm = False

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            confirm = True

    context = {
        'profile': profile,
        'form': form,
        'confirm': confirm,
    }

    return render(request, 'profiles/my_profile.html', context)


@login_required
def inviteRecievedView(request):
    profile = Profile.objects.get(user=request.user)
    relations = Relationship.objects.invitationReciever(profile)
    names_sender = list(map(lambda x: x.sender, relations))
    is_empty = False
    if len(names_sender) == 0:
        is_empty = True
    context = {
        'names_sender': names_sender,
        'is_empty': is_empty,
    }

    return render(request, 'profiles/my_invites.html', context)


@login_required
def inviteListProfilesView(request):
    user = request.user
    profiles = Profile.objects.getAllProfileToInvite(user)

    context = {
        'profiles': profiles,
    }

    return render(request, 'profiles/invite_list_profiles.html', context)


# def listProfilesView(request):
#     user = request.user
#     profiles = Profile.objects.getAllProfiles(user)

#     context = {
#         'profiles': profiles,
#     }

#     return render(request, 'profiles/list_profiles.html', context)


class DetailProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'profiles/detail_profile.html'
    context_object_name = 'profile'

    def get_object(self, slug=None):
        slug = self.kwargs.get('slug')
        profile = Profile.objects.get(slug=slug)
        return profile

    def get_context_data(self, *args, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile_ = Profile.objects.get(user=user)
        rel_s = Relationship.objects.filter(sender=profile_)
        rel_r = Relationship.objects.filter(reciever=profile_)
        rel_sender = []
        rel_reciever = []
        for item in rel_s:
            rel_reciever.append(item.reciever.user)
        for item in rel_r:
            rel_sender.append(item.sender.user)
        extra_context = {
            'rel_sender': rel_sender,
            'rel_reciever': rel_reciever,
            'posts': self.get_object().getAllPosts,
            'len_posts': True if len(self.get_object().getAllPosts) > 0 else False,
        }
        context.update(extra_context)
        return context


class ListProfileView(LoginRequiredMixin, ListView):
    model = Profile
    template_name = 'profiles/list_profiles.html'
    context_object_name = 'profiles'

    def get_queryset(self):
        profiles = Profile.objects.getAllProfiles(self.request.user)
        return profiles

    def get_context_data(self, *args, **kwargs):
        kwargs = self.kwargs
        context = super().get_context_data(**kwargs)
        user = User.objects.get(username__iexact=self.request.user)
        profile_ = Profile.objects.get(user=user)
        rel_s = Relationship.objects.filter(sender=profile_)
        rel_r = Relationship.objects.filter(reciever=profile_)
        rel_sender = []
        rel_reciever = []
        for item in rel_s:
            rel_reciever.append(item.reciever.user)
        for item in rel_r:
            rel_sender.append(item.sender.user)
        is_empty = False
        if len(self.get_queryset()) == 0:
            is_empty = True
        extra_context = {
            'profile_': profile_,
            'rel_sender': rel_sender,
            'rel_reciever': rel_reciever,
            'is_empty': is_empty,
        }
        context.update(extra_context)
        return context


@login_required
def sendInvitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender_ = Profile.objects.get(user=request.user)
        reciever_ = Profile.objects.get(pk=pk)
        relationship = Relationship.objects.create(
            sender=sender_, reciever=reciever_, status='send')

        # it's same current url or profiles:list-profiles
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile')


@login_required
def acceptInvitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender_ = Profile.objects.get(pk=pk)
        reciever_ = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(
            Relationship, sender=sender_, reciever=reciever_)
        if relationship.status == 'send':
            relationship.status = 'accepted'
            relationship.save()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile')


@login_required
def rejectInvitation(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender_ = Profile.objects.get(pk=pk)
        reciever_ = Profile.objects.get(user=request.user)
        relationship = get_object_or_404(
            Relationship, sender=sender_, reciever=reciever_)
        if relationship.status == 'send':
            relationship.delete()
        return redirect(request.META.get('HTTP_REFERER'))
    return redirect('profiles:my-profile')


@login_required
def deleteFriend(request):
    if request.method == 'POST':
        pk = request.POST.get('profile_pk')
        sender_ = Profile.objects.get(user=request.user)
        reciever_ = Profile.objects.get(pk=pk)
        relationship = Relationship.objects.get((Q(sender=sender_) & Q(
            reciever=reciever_)) | (Q(sender=reciever_) & Q(reciever=sender_)))

        relationship.delete()

        # it's same current url or profiles:list-profiles
        # return redirect(request.META.get('HTTP_REFERER'))
        return redirect('profiles:list-profiles')
    return redirect('profiles:my-profile')
