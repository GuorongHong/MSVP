from django.http import HttpResponse, HttpResponseRedirect
from .models import Passwords
from .forms import PasswordForm, GeneratePasswordForm
from django.template import loader
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string 
import string


def index(request):
    template = loader.get_template('password/index.html')
    if request.user.is_authenticated:
        data = Passwords.objects.filter(user = request.user)
        context = {
        'data': data,
        }
    else:
        context = {}
    return HttpResponse(template.render(context, request))

def add_pw(request):
    if request.method == 'POST':
        form = PasswordForm(request.POST)
        if form.is_valid():
            s = Passwords()
            s.userid = form.cleaned_data['userid']
            s.pw = form.cleaned_data['pw']
            s.web = form.cleaned_data['web']
            s.user = request.user 
            s.save()
            return redirect('index')
    else:
        form = PasswordForm()
    return render(request, 'password/add_pw.html', {'form': form})
    
def del_pw(request, id):
    obj = Passwords.objects.get(id = id)
    if request.method == 'POST':
        if obj.user.id == request.user.id:
            obj.delete()
            return redirect('../../')
        return HttpResponse('No Permission')
    context = {
        'object': obj
    }
    return render(request, "password/del_pw.html", context)

similar_chars = {'o', 'O', '0', 'I', 'l', '1', '|'}

def generate_pw(request):
    form = GeneratePasswordForm(request.POST or None)
    if not form.is_valid():
        context = {'password' : 'Your password will show here', 'length': 12, 'form': form}
    else:
        data = form.cleaned_data
        charset = ''
        if data['use_lower']:
            charset += string.ascii_lowercase
        if data['use_upper']:
            charset += string.ascii_uppercase
        if data['use_digits']:
            charset += string.digits
        if data['use_special']:
            charset += string.punctuation
        if data['avoid_similar']:
            charset = [c for c in charset if c not in similar_chars]
        length = data['length']
        password = get_random_string(length, charset)
        context = {'password': password, 'length': length, 'form': form}
    return render(request, 'password/generate_pw.html', context)