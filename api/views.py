from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from .serializers import UserSerializer

import json


# Create your views here.
@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'List': '/user-list/',
        'Detail': 'user-detail<str:pk>',
        'Create': '/task-create',
    }

    return Response(api_urls)


@api_view(['GET'])
def userList(request):
    lst = User.objects.all()
    serializer = UserSerializer(lst, many=True)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['GET'])
def userDetail(request, uname):
    user = User.objects.get(username=uname)
    serializer = UserSerializer(user, many=False)
    return Response(
        serializer.data,
        status=status.HTTP_200_OK
    )


@api_view(['POST'])
def userCreate(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()

    return Response(
        serializer.id,
        serializer.data,
        status=status.HTTP_201_CREATED
    )


@api_view(['POST'])
def userLogin(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')

    if username is None or password is None:
        return Response(
            {'detail': 'Provide username and password'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user = User.objects.get(username=username)
    if user.password != password:
        user = None
    # user = authenticate(username=username, password=password)

    if user is None:
        return Response(
            {'detail': 'Invalid credentials'},
            status=status.HTTP_400_BAD_REQUEST
        )

    return Response(
        {'username': username},
        status=status.HTTP_200_OK
    )
