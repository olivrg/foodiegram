from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()


class MemberFormPersonal(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', ]


class MemberProfilePhotoForm(forms.ModelForm):
    image_errors = {'required': 'Please upload your profile image', }

    profile_image = forms.ImageField(
        label='Select a image', error_messages=image_errors)

    class Meta:
        model = User
        fields = ['profile_image', ]

    def __ini__(self, *args, **kwargs):
        super(MemberProfilePhotoForm, self).__init__(*args, **kwargs)

        for key in self.fields:
            self.fields[key].required = True
