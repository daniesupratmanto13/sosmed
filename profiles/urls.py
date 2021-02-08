from django.urls import path


# own function
from .views import *

app_name = 'profiles'

urlpatterns = [
    path('', ListProfileView.as_view(), name='list-profiles'),
    path('detail/<slug>/', DetailProfileView.as_view(), name='detail-profile'),
    path('my_profile', myProfileView, name='my-profile'),
    path('my_invites/', inviteRecievedView, name='my-invites'),
    path('invite_list_profiles/', inviteListProfilesView,
         name='invite-list-profiles'),

    path('send_invite/', sendInvitation, name='send-invite'),
    path('delete_friend/', deleteFriend, name='delete-friend'),
    path('my_invites/accept/', acceptInvitation, name='accept-invite'),
    path('my_invites/reject/', rejectInvitation, name='reject-invite'),
]
