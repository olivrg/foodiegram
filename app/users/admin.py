from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.models import Group
from django.utils.translation import gettext as _

from users.models import User


class UserCreationForm(forms.ModelForm):
    """form to create new users"""
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ("email",)

    def clean_password2(self):
        # check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        # save the provided password in hashed format
        user = super(UserCreationForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """update users"""
    password = ReadOnlyPasswordHashField(
        label=("Password"),
        help_text=(
            "Raw passwords are not stored, so there is no way to see "
            "this user's password, but you can change the password "
            "using <a href=\'../password/\'>this form</a>."
        )
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password')

    def clean_password(self):
        return self.initial['password']


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # user model fields
    list_display = ['email', 'username',
                    'favourite_dish', 'random_user_id', 'name',
                    'is_staff', 'is_active'
                    ]
    read_only_fields = ('random_user_id',)
    fieldsets = (
        (None, {'fields': ('password',)}),
        ('Personal Info', {'fields': (
            'name',
            'email',
            'phone_number',
            'gender',
            'favourite_dish',
            'reset_password_token',

        )}),
        ('Site Info', {'fields': (
            'username',
            'profile_picture',
            'following',
            'followers',
            'is_staff',
            'is_active',
            'is_superuser',
            'groups',
            'user_permissions',
            'last_login',
        )}),
    )

    # override get_fieldsets to use this attribute when creating a user
    add_fieldsets = (
        (None, {'fields': (
            'username',
            'password1',
            'password2',
        )}),
        ('Personal Info', {'fields': (
            'email',
            'name',
        )}),
    )

    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


admin.site.register(User, UserAdmin)
admin.site.unregister(Group)
