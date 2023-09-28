from django.forms import ModelForm, CharField
from django import forms
from django.contrib.auth.forms import UserChangeForm
from .models import Room, Message, Topic, UserProfile
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


class CustomUserChangeForm(UserChangeForm):
    old_password = forms.CharField(
        label="Current Password", widget=forms.PasswordInput, required=False)
    new_password = forms.CharField(
        label="New Password", widget=forms.PasswordInput, required=False)

    class Meta:
        model = User
        fields = ('username', 'old_password', 'new_password')

    def clean_new_password(self):
        new_password = self.cleaned_data.get('new_password')
        if new_password:
            password_validation.validate_password(new_password, self.instance)
        return new_password


class RoomForm(ModelForm):
    topic = CharField(max_length=200)

    class Meta:
        model = Room
        fields = ['name', 'topic', 'description', 'private']

    def clean_topic(self):
        topic_name = self.cleaned_data['topic']
        topic, created = Topic.objects.get_or_create(name=topic_name)
        return topic


class ProfileCreationForm(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email']


class ProfileEditform(ModelForm):
    class Meta:
        model = UserProfile
        fields = ['email', 'pfp', 'bio']
