from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Skill


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['first_name', 'email', 'username', 'password1', 'password2']
        labels = {
            'first_name': 'Name',
        }

    def __init__(self, *args, **kwargs):
        super(CustomUserCreationForm, self).__init__(*args, **kwargs)

        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'input'})


class Profileform(ModelForm):
    class Meta:
        model = Profile
        fields = '__all__'
        exclude = ['user']

    def __init__(self, *args, **kwargs):
        super(Profileform, self).__init__(*args, **kwargs)

        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'input'})


class SkillForm(ModelForm):
    class Meta:
        model = Skill
        fields = '__all__'
        exclude = ['owner']

    def __init__(self, *args, **kwargs):
        super(SkillForm, self).__init__(*args, **kwargs)

        for k, v in self.fields.items():
            v.widget.attrs.update({'class': 'input'})
