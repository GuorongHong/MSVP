from django.http import HttpResponse, HttpResponseRedirect
from django.db.models import Q
from django.template import loader
from django.shortcuts import render, redirect
from django.utils.crypto import get_random_string, pbkdf2, salted_hmac
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.contrib.auth import logout
from django.contrib.postgres.search import TrigramSimilarity
from django.db.models.functions import Greatest
from django_otp.decorators import otp_required
from django.contrib.auth.decorators import login_required

from .models import Passwords
from .forms import PasswordForm, GeneratePasswordForm

from Crypto.Cipher import AES

from random import randint
import string

@login_required
def index(request):
    if 'cipherKey' not in request.session:
        return redirect('verify_pw')
    template = loader.get_template('password/index.html')
    if request.user.is_authenticated:
        data = Passwords.objects.filter(user = request.user)
        for obj in data:
            encryption_suite = AES.new(bytes.fromhex(request.session.get('cipherKey')), AES.MODE_CFB, bytes.fromhex(request.session.get('iv')))
            obj.pw = encryption_suite.decrypt(bytes.fromhex(obj.pw)).decode('utf-8')
        context = {
        'data': data,
        }
    else:
        context = {}
    return HttpResponse(template.render(context, request))

@login_required
def edit(request, id):
    if 'cipherKey' not in request.session:
        return redirect('verify_pw')
    obj = Passwords.objects.get(id = id)
    if request.method == 'POST' and request.POST.get('npw'):
        encryption_suite = AES.new(bytes.fromhex(request.session.get('cipherKey')), AES.MODE_CFB, bytes.fromhex(request.session.get('iv')))
        obj.pw = encryption_suite.encrypt(request.POST.get('npw').encode('utf-8')).hex()
        obj.save()
        return redirect('/password/')
    encryption_suite = AES.new(bytes.fromhex(request.session.get('cipherKey')), AES.MODE_CFB, bytes.fromhex(request.session.get('iv')))
    obj.pw = encryption_suite.decrypt(bytes.fromhex(obj.pw)).decode('utf-8')
    return render(request, 'password/edit.html', {'obj': obj})

@login_required
def add_pw(request):
    password = 'Generated password'
    length = 8
    if 'cipherKey' not in request.session:
        return redirect('verify_pw')
    if request.method == 'POST' and 'GenerateSubmit' in request.POST:
        addform = PasswordForm(request.POST, prefix='add')
        generateform = GeneratePasswordForm(request.POST or None, prefix='generate')
        if generateform.is_valid():
            data = generateform.cleaned_data
            length = data['length']
            charset = ''
            personal_str = data['personal_details']
            # check if personal details were included
            if personal_str != '':
                # from the string, get list with each word as an item
                personal_lst = str(personal_str).split(",")
                # length of characters of personal words inputted
                personal_length = len(personal_str)
                for char in personal_str:
                    if char == ",":
                        personal_length -= 1
                # check if number of characters in personal details exceeds length set
                if personal_length > length:
                    password = "Length of personal details exceed password length!"
                else:
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
                    # randomly generate password without details, then afterwards 
                    # randomly insert the items in personal_arr into the password generated
                    length -= personal_length
                    before_password = get_random_string(length, charset)

                    for item in personal_lst:
                        pos = randint(0, len(before_password) - 1)  # pick random position to insert item
                        before_password = "".join((before_password[:pos], item, before_password[pos:])) # insert item at pos                    
                    
                    password = before_password
            else:
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
                password = get_random_string(length, charset)
                
    if request.method == 'POST' and 'AddSubmit' in request.POST:
        addform = PasswordForm(request.POST, prefix='add')
        generateform = GeneratePasswordForm(request.POST or None, prefix='generate')
        if addform.is_valid():
            encryption_suite = AES.new(bytes.fromhex(request.session.get('cipherKey')), AES.MODE_CFB, bytes.fromhex(request.session.get('iv')))
            s = Passwords()
            s.userid = addform.cleaned_data['userid']
            s.pw = encryption_suite.encrypt(addform.cleaned_data['pw'].encode('utf-8')).hex()
            s.web = addform.cleaned_data['web']
            s.email = addform.cleaned_data['email']
            s.user = request.user 
            s.save()
            return redirect('/password/')
    else:
        addform = PasswordForm(prefix='add')
        generateform = GeneratePasswordForm(prefix='generate')

    extra_context = {
        'add_form':PasswordForm(prefix='add'),
        'generate_form':GeneratePasswordForm(prefix='generate'),
        'password':password, 'length':length,
    }
    return render(request, 'password/add_pw.html', extra_context)

@login_required    
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

@login_required
def verify_pw(request):
    if request.method == 'POST':
        if check_password(request.POST.get("Password"), request.user.password):
            _, _, salt, _ = request.user.password.split('$')
            key = pbkdf2(request.POST.get("Password"), salt, 50000, 48)
            request.session['iv'] = key[0:16].hex()
            request.session['cipherKey'] = key[16:].hex()
            return redirect('/password/')
        else:
            return HttpResponse('Incorrect Password')
    return render(request, "password/verify_pw.html", {})

@login_required
def search(request):
    if request.method == 'GET':
        query = request.GET.get('q')
        results = Passwords.objects.filter(user = request.user)
        results = results.annotate(similarity = TrigramSimilarity('web', query)).filter(similarity__gt = 0.1).order_by('-similarity')
        for obj in results:
            encryption_suite = AES.new(bytes.fromhex(request.session.get('cipherKey')), AES.MODE_CFB, bytes.fromhex(request.session.get('iv')))
            obj.pw = encryption_suite.decrypt(bytes.fromhex(obj.pw)).decode('utf-8')
        return render(request, 'password/search.html', {'results':results})
    else:
        return render(request, 'password/search.html', {})

@login_required
def change_pw(request):
    if request.method == 'POST' and request.user.is_authenticated:
            if 'cipherKey' not in request.session:
                return redirect('verify_pw')
            data = Passwords.objects.filter(user = request.user)
            u = User.objects.get(username = request.user.username)
            u.set_password(request.POST.get('new_pw'))
            u.save()
            _, _, salt, _ = u.password.split('$')
            key = pbkdf2(request.POST.get("new_pw"), salt, 50000, 48)
            key,iv = key[16:], key[0:16]
            for obj in data:
                encryption_suite = AES.new(bytes.fromhex(request.session.get('cipherKey')), AES.MODE_CFB, bytes.fromhex(request.session.get('iv')))
                obj.pw = encryption_suite.decrypt(bytes.fromhex(obj.pw)).decode('utf-8')
                new_encryption_suite = AES.new(key, AES.MODE_CFB, iv)
                obj.pw = new_encryption_suite.encrypt(obj.pw.encode('utf-8')).hex()
                obj.save()
            logout(request)
            return redirect('login')
    else:
        return render(request, 'password/change_pw.html', {})
