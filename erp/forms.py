from django.contrib.auth.forms import UserCreationForm
from django.forms import ModelForm
from django import forms
from django.contrib.auth.models import User, Group

from erp.models import Employee

class PasswordInputWithPlaceholder(forms.PasswordInput):
    def __init__(self, attrs=None):
        super().__init__(attrs={'class': 'form-control', 'placeholder': 'Password'})

# class CreateUserForm(UserCreationForm):
#     employee_choices = [(employee.person_farm_entity.farm_entity_id, f"{employee.person_farm_entity.first_name} {employee.person_farm_entity.last_name}") for employee in Employee.objects.all()]
#     employee_id = forms.ChoiceField(choices=employee_choices, widget=forms.Select(attrs={'class': 'form-control'}))

#     class Meta(UserCreationForm.Meta):
#         model = User
#         fields = ['username', 'email', 'password1', 'password2', 'employee_id']
#         widgets = {
#             'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
#             'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
#         }

#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
#         self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})

class CreateUserForm(UserCreationForm):
    employee_id = forms.ChoiceField(choices=[], widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'employee_id']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm Password'})
        self.fields['employee_id'].choices = self.get_employee_choices()

    def get_employee_choices(self):
        return [(employee.person_farm_entity.farm_entity_id, f"{employee.person_farm_entity.first_name} {employee.person_farm_entity.last_name}") for employee in Employee.objects.all()]


class GroupCreationForm(forms.ModelForm):
    class Meta:
        model = Group
        fields = ['name', 'permissions']  
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'role'}),
        }

class GroupAssignmentForm(forms.Form):
    group = forms.ModelChoiceField(queryset=Group.objects.all())
    user = forms.ModelChoiceField(queryset=User.objects.all())