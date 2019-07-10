# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.template import loader
from django.views import generic
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect

from .forms import SignUpForm, GetHintForm
from .models import PasswordHint

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
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
        'username': data.username
        }
        return render(request, 'hint.html', context)

    if request.method == 'POST':
        form = GetHintForm(request.POST)
        # check if username matches any in the db
        if form.is_valid():
            name_input = request.POST['username']
            if GetHintForm().username_present(name_input) != False:
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
        data = PasswordHint.objects.get(username=name_input)
        if data.hint != "No hint available":
            current_hint = data.hint
        else:
            current_hint = False
        if request.method == 'POST':
            if request.POST['new_hint'] == '':
                data.hint = "No hint available"
            else:
                data.hint = request.POST['new_hint']
            data.save()
            return redirect('/password/')
    return render(request, 'add_hint.html', {'data':data, 'current_hint':current_hint})