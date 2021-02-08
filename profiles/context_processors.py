from .models import Profile, Relationship


def profilePic(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        picture = profile.avatar
        return {
            'picture': picture,
        }
    return {}


def inviteRecievedCount(request):
    if request.user.is_authenticated:
        profile = Profile.objects.get(user=request.user)
        invite_recieved_count = Relationship.objects.invitationReciever(
            profile).count()
        return {
            'invite_recieved_count': invite_recieved_count
        }
    return {}
