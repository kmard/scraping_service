
# https://docs.djangoproject.com/en/3.0/topics/auth/default/

from django import forms
from django.contrib.auth import get_user_model,authenticate
from django.contrib.auth.hashers import check_password

User = get_user_model()

class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput(attrs={'class':'form-comtrol'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-comtrol'}))

    def clean(self, *args,**kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('User is not defined !')

            if not check_password(password,qs[0].password):
                raise forms.ValidationError('Wrong password !')

            user = authenticate(email=email,password=password)
            if not user:
                raise forms.ValidationError('Account is disabled !')

            return super(UserLoginForm,self).clean(*args,**kwargs)

class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(label='enter email',
        widget=forms.EmailInput(attrs={'class':'form-comtrol'}))
    password = forms.CharField(label='enter password',
        widget=forms.PasswordInput(attrs={'class':'form-comtrol'}))
    password2 = forms.CharField(label='repeat password',
        widget=forms.PasswordInput(attrs={'class': 'form-comtrol'}))

    class Meta:
        model = User
        fields = ('email',)

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Passwords are different!')
        else:
            return data['password2']


