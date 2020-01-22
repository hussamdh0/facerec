from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from home.models import Profile, User
from django.contrib.auth import authenticate, login, logout
import socket

HOST = '127.0.0.1'
PORT = 3002


def index(request):
    mth = request.method
    if mth == 'POST':
        try:
            usr = request.POST['loginUsername']
            psw = request.POST['loginPassword']
            user = authenticate(request, username=usr, password=psw)
            if user is None:
                template = loader.get_template('website/index.html')
                return HttpResponse(template.render(
                    {'Err': 'No Such Username Exists or Password is incorrect'}, request))
        except:
            user = None
        if user is not None:
            login(request, user)
            template = loader.get_template('website/indexNoRec.html')
            return HttpResponse(template.render({}, request))
        else:
            try:
                print(request.COOKIES['facetoken'])
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.connect((HOST, PORT))
                s.send(('do you have this token?,' + request.COOKIES['facetoken']).encode())
                response = s.recv(1024)
                response = response.decode('ascii').split(',')
                s.send(('close').encode())
                s.close()
                print(response)
                if response[0] == 'yes I do':
                    login(request, User.objects.get(pk=int(response[1])))
                    template = loader.get_template('website/indexNoRec.html')
                    return HttpResponse(template.render({}, request))
                else:
                    template = loader.get_template('website/index.html')
                    return HttpResponse(template.render({'ex': 1}, request))
            except:
                print('facetoken not found!')
    else:
        template = loader.get_template('website/index.html')
        return HttpResponse(template.render({'ex': 0}, request))
