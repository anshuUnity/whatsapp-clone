from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse

# Create your views here.

User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)

        if form.is_valid():
            new_user = form.save()
            new_user = authenticate(username=form.cleaned_data['username'],
                                    password=form.cleaned_data['password1'],
                                    )
            login(request, new_user)

            return HttpResponseRedirect(reverse('home'))

    else:
        form = SignUpForm()

    return render(request, 'accounts/register.html', {'form': form})


def loginView(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('home'))

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect(reverse('home'))
            else:
                return HttpResponse("Account Not Active")
        else:
            context = {'notfound': True}
            print(
                f"NO ACCOUNT FOUND WITH USERNAME {username} AND PASSWORD {password}")
            print(context)
            return render(request, 'accounts/login.html', context)

    else:
        return render(request, 'accounts/login.html')
