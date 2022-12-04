import re

from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


def add_attr(field, attr_name, attr_new_val):
    existing = field.widget.attrs.get(attr_name, '')
    field.widget.attrs[attr_name] = f'{existing} {attr_new_val}'.strip()

def add_placeholder(field, placeholder_val):
    add_attr(field, 'placeholder', placeholder_val)

def strong_password(password):
    regex = re.compile(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*[0-9]).{8,}$')

    if not regex.match(password):
        raise ValidationError((
            'Senha tem que ter uma letra minuscula, maiscula e um numero'
        ),
         code= 'Invalid'
        )

class RegisterForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        add_placeholder(self.fields['username'], 'Seu nome de usuario')

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
                'placeholder': 'Coloque sua senha'
            }),
        validators=[strong_password]
    )
    password2 = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Repeat your password'
        })
    )
    class Meta:
        model = User
        fields = [
            'first_name',
            'last_name',
            'username',
            'email',
            'password'
        ]
        #exclude = ['first_name']
        labels = {
            'username': 'digite seu usuário'
        }
        help_texts = {
            'email': 'Email deve ser valido'
        }
        error_messages = {
            'username': {
                'invalid': 'Esse username é invalido'
            }
        }
        widgets = {
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Coloque seu primeiro nome',
                'class': 'form-control'
            })
        }
        # validators = {
        #     'password': [strong_password]
        # }
    
    #especifico do campo
    def clean_password(self):
        data = self.cleaned_data.get('password')

        # if 'atenção' in data: SÓ UM EXEMPLO
        #     raise ValidationError(
        #         'Não digite %(value)s no campo password',
        #         code='invalid',
        #         params={'value': '"atenção"'}
        #     )
        return data

    #valida todos os campos, não é um campo especifico
    def clean(self):
        cleaned_data = super().clean()

        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')

        if password != password2:
            password_confirmation_error = ValidationError(
                'Password and password2 must be equal'
                # code='invalid'
            )
            raise ValidationError({
                'password': password_confirmation_error,
                'password2': [
                    password_confirmation_error,
                ],
            })