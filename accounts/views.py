# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.template import loader
from django.views import generic
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .models import PasswordHint
from .forms import SignUpForm, GetHintForm, AddHintForm

from .forms import SignUpForm, GetHintForm
from .models import PasswordHint

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            p = PasswordHint()
            ## set defaults for when no hint inputted
            p.username = request.user.username
            p.hint = "No hint available"
            p.save()
            form.save()
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

## retrieve hint when user forgets pw

def login_hint(request):

    def retrieve_hint(request):
        data = PasswordHint.objects.get(username=name_input)
        hint = data.hint
        username = data.username
        context = {
            'data': data,
            'hint': hint,
            'username': username
        }
        return render(request, 'hint.html', context)

    if request.method == 'POST':
        form = GetHintForm(request.POST)
        # check if username matches any in the db
        if form.is_valid():
            name_input = form.cleaned_data['username']
            if form.username_present(name_input) != False:
                return retrieve_hint(request)
            else:
                return HttpResponse('No such username')
    else:
        form = GetHintForm()
    return render(request, 'login_hint.html', {'form': form})

def add_hint(request):
    if 'cipherKey' not in request.session:
        return redirect('verify_pw')

    if request.user.is_authenticated:
        name_input = request.user.username
        ## check if there is any hint tagged to the username adn show it
        ## if not, create default new one and show that instead
        check = PasswordHint.objects.get_or_create(
            username=name_input,
            defaults={
                'username':name_input,
                'hint':"No hint available"
            }
        )
        data = PasswordHint.objects.get(username=name_input)
        if data.hint == "No hint available" or data.hint == '':
            current_hint = False
        else:
            current_hint = data.hint

        if request.method == 'POST':
            form = AddHintForm(request.POST)
            if form.is_valid():
                if request.POST['new_hint'] == '':
                    data.hint = "No hint available"
                else:
                    ## is there something wrong here wtf
                    data.hint = form.cleaned_data['new_hint']
                data.save()
                return redirect('index')

        context = {
            'data':data, 
            'current_hint':current_hint
            }
    else:
        context = {}
    return render(request, 'add_hint.html', context)