from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from accounts.forms import UserLoginForm, UserRegistrationForm, UserUpdateForm, ContactForm
from django.contrib import messages
import datetime as dt
from scrapping.models import Error

User = get_user_model()

def login_view(request):
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        data = form.cleaned_data
        email = data.get('email')
        password = data.get('password')

        user = authenticate(request,email=email,password=password)

        login(request,user)
        return redirect('home')
        # return LOGIN_REDIRECT_URL = '/accounts/profile/'
    return render(request,'accounts/login.html',{'form':form})

def logout_view(request):
    logout(request)
    return redirect('home')

def register_view(request):
    form = UserRegistrationForm(request.POST or None)
    if form.is_valid():
        new_user = form.save(commit=False)
        new_user.set_password(form.cleaned_data['password'])
        new_user.save()
        # https://docs.djangoproject.com/en/4.0/ref/contrib/messages/
        messages.success(request, 'New user is registered')
        return render(request,'accounts/register_done.html',{'new_user':new_user})

    return render(request, 'accounts/register.html', {'form': form})

def update_view(request):
    contact_Form = ContactForm()
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            form = UserUpdateForm(request.POST)
            if form.is_valid():
                date = form.cleaned_data
                user.city = date['city']
                user.language = date['language']
                user.send_email = date.get('send_email')
                user.save()
                return redirect('accounts:update')


        form = UserUpdateForm(
            initial={'city':user.city,
                     'language':user.language,
                     'send_email':user.send_email})
        return render(request, 'accounts/update.html',
                      {'form': form,'contact_Form': contact_Form})
    else:
        return redirect('accounts:login')

def delete_view(request):
    if request.user.is_authenticated:
        user = request.user
        if request.method == 'POST':
            qs = User.objects.get(pk=user.pk)
            qs.delete()
    return redirect('home')

def contact(request):
    if request.method == 'POST':
        contact_form = ContactForm(request.POST or None)
        if contact_form.is_valid():
            data = contact_form.cleaned_data
            city = data.get('city')
            language = data.get('language')
            email = data.get('email')
            qs = Error.objects.filter(timestamp=dt.date.today())
            if qs.exists():
                err = qs.first()
                data = err.data.get('user_data', [])
                data.append({'city': city, 'email': email, 'language': language})
                err.data['user_data'] = data
                err.save()
            else:
                data = {'user_data': [
                    {'city': city, 'email': email, 'language': language}
                ]}
                Error(data=data).save()
            messages.success(request, 'Данные отправлены администрации.')
            return redirect('accounts:update')
        else:
            return redirect('accounts:update')
    else:
        return redirect('accounts:login')
