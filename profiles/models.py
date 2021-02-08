from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse
from django.db.models import Q

# My class and function
from .utils import getRandomCode, userAvatarPath

# third party
from PIL import Image


class ProfileManager(models.Manager):

    def getAllProfiles(self, me):
        profiles = Profile.objects.all().exclude(user=me)
        return profiles

    def getAllProfileToInvite(self, sender):
        profiles = Profile.objects.all().exclude(user=sender)
        profile = Profile.objects.get(user=sender)
        relations = Relationship.objects.filter(
            Q(sender=profile) | Q(reciever=profile))
        print(relations)
        accepted = set([])

        for relation in relations:
            if relation.status == 'accepted':
                accepted.add(relation.sender)
                accepted.add(relation.reciever)
        print(accepted)

        available = [
            profile for profile in profiles if profile not in accepted]
        print(available)
        return available


class Profile(models.Model):
    first_name = models.CharField(max_length=200, blank=True)
    last_name = models.CharField(max_length=200, blank=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(default='no bio.....', max_length=300)
    email = models.EmailField(max_length=200, blank=True)
    country = models.CharField(max_length=200, blank=True)
    avatar = models.ImageField(default='avatar.png', upload_to=userAvatarPath)
    friends = models.ManyToManyField(User, blank=True, related_name='friends')
    slug = models.SlugField(unique=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = ProfileManager()

    @property
    def getAllFriends(self):
        return self.friends.all()

    @property
    def getFriendsCount(self):
        return self.friends.all().count()

    @property
    def getAllPosts(self):
        return self.post.all()

    @property
    def getPostsCount(self):
        return self.post.all().count()

    @property
    def getLikeGivenCount(self):
        likes = self.like_set.all()
        total_like = 0
        for vote in likes:
            if vote.value == 'Like':
                total_like += 1
        return total_like

    @property
    def getLikedRecievedCount(self):
        posts = self.post.all()
        total_liked = 0
        for post in posts:
            total_liked += post.liked.all().count()
        return total_liked

    @property
    def getURL(self):
        return reverse("profiles:detail-profile", kwargs={"slug": self.slug})

    __init_first_name = None
    __init_last_name = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__init_first_name = self.first_name
        self.__init_last_name = self.last_name

    def __str__(self):
        return f"{self.id}-{self.user}"

    def save(self, *args, **kwargs):
        SIZE = (250, 250)
        ex = False
        to_slug = self.slug
        if self.first_name != self.__init_first_name or self.last_name != self.__init_last_name or self.slug == "":
            if self.first_name and self.last_name:
                to_slug = slugify(str(self.first_name) +
                                  ' ' + str(self.last_name))
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + ' ' + getRandomCode())
                    ex = Profile.objects.filter(slug=to_slug).exists()
            else:
                to_slug = str(self.user)
                ex = Profile.objects.filter(slug=to_slug).exists()
                while ex:
                    to_slug = slugify(to_slug + ' ' + getRandomCode())
                    ex = Profile.objects.filter(slug=to_slug).exists()
        self.slug = to_slug
        super().save(*args, **kwargs)

        if self.avatar:
            pic = Image.open(self.avatar.path)
            pic.thumbnail(SIZE, Image.LANCZOS)
            pic.save(self.avatar.path)

    class Meta:
        ordering = ('created',)


STATUS_CHOICES = (
    ('send', 'send'),
    ('accepted', 'accepted'),
)


class RelationshipManager(models.Manager):
    def invitationReciever(self, reciever):
        relation = Relationship.objects.filter(
            reciever=reciever, status='send')
        return relation


class Relationship(models.Model):
    sender = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='sender')
    reciever = models.ForeignKey(
        Profile, on_delete=models.CASCADE, related_name='reciever')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    objects = RelationshipManager()

    def __str__(self) -> str:
        return '{} to {}-{}'.format(self.sender, self.reciever, self.status)
