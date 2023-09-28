from django.urls import path, include
# views folder
from .views import home, profile, room_messages, register_login, profile, rooms, forgot_pwd, guestest, convert, join_leave_room
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('', home.home, name='home'),
    path('room/<str:pk>', room_messages.room, name='room'),
    path('create-room/', rooms.createRoom, name='create-room'),
    path('update-room/<str:pk>', rooms.updateRoom, name='update-room'),
    path('delete-room', rooms.deleteRoom, name='delete-room'),
    path('login/', register_login.LoginPage, name='login'),
    path('logout/', register_login.LogoutPage, name='logout'),
    path('register/', register_login.RegisterPage, name='register'),
    path('delete-msg', room_messages.deleteMessage, name='delete-msg'),
    path('edit-msg', room_messages.EditMessage, name='edit-msg'),
    path('profile/<str:pk>', profile.Profile, name='profile'),
    path('joined-rooms', profile.JoinedRooms, name='joined-rooms'),
    path('account', profile.AccountSettings, name='account'),
    path('forgot', forgot_pwd.ForgotPwd, name='forgot'),
    path("convert/", convert.custom_convert_form, name='guest_user_convert'),
    path('guest', guestest.welcome_user, name='guest_user_convert_success'),
    path('confirm_logout', guestest.ConfirmLogout, name="confirm-logout"),
    path('leave_room', rooms.LeaveRoom, name="leave-room"),
    path('join_room', rooms.JoinRoom, name="join-room"),
    path('invite/<str:code>', rooms.Invite, name='invite'),
    path('invite', rooms.InvitePage, name='invite-room'),
    path('join/<str:code>', rooms.InviteJoin, name='join'),
    path('load_messages', room_messages.LoadMessages, name='load-messages')

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
