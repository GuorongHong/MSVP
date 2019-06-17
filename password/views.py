from django.http import HttpResponse, HttpResponseRedirect
from .models import Passwords
from .forms import PasswordForm
from django.template import loader
from django.shortcuts import render, redirect


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

