from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Profile
from django.contrib.auth import authenticate, login, logout
import socket


HOST = '127.0.0.1'
PORT = 3002


def index(request):
    all_users = Profile.objects.all()
    try:
        print(request.COOKIES['facetoken'])
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(('do you have this token?,' + request.COOKIES['facetoken']).encode())
        response = s.recv(1024)
        s.send(('close').encode())
        s.close()
        print(response)
    except:
        print('facetoken not found!')

    context = {'all_users': all_users}

    template = loader.get_template('home/index.html')
    return HttpResponse(template.render(context, request))


def user(request):
    # login(request, Profile.objects.all()[1].user)
    # logout(request)
    print('user', request.user.pk)
    template = loader.get_template('home/user.html')
    return HttpResponse(template.render({}, request))


def lists(request):
    template = loader.get_template('home/lists.html')
    return HttpResponse(template.render({'posts' : Profile.objects.all()}, request))


def detail(request, user_id):
    return HttpResponse('<h2> NICE WORK, Request With ID: ' + user_id + '<h2>')