from django.contrib.admin import site
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group
from django.core.mail import EmailMessage
from django.forms import ModelForm
from django.utils.crypto import get_random_string
from .models import User


class UserCreationForm(ModelForm):
    class Meta:
        model = User
        fields = ('email',)

    def save(self, commit=True):
        user = super().save(commit=False)
        password = get_random_string()
        user.set_password(password)
        EmailMessage('Raions account password', password, to=[user.email]).send()
        if commit:
            user.save()
        return user


class UserChangeForm(ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ('email', 'is_active', 'is_staff')


class UserAdmin(BaseUserAdmin):
    add_form = UserCreationForm
    form = UserChangeForm
    list_display = ('email', 'is_staff')
    list_filter = ('is_staff',)
    add_fieldsets = (
        (None, {'classes': ('wide',), 'fields': ('email',)}),
    )
    fieldsets = (
        (None, {'fields': ('email',)}),
        ('Permissions', {'fields': ('is_staff',)})
    )
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ()


site.register(User, UserAdmin)
site.unregister(Group)
