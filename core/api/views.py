from datetime import datetime

import requests
from django.conf import settings
from django.db.models import Window, F, Max
from django.db.models.functions import Rank
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .serializer import *
from .models import *
from rest_framework import generics, status
from rest_framework.response import Response
import jwt


import rest_framework_simplejwt


# Create your views here.


class RegisterAPIView(APIView):
    def post(self, request):
        serializer = EmployeeSerializer(data=request.data)
        if serializer.is_valid():
            try:
                Employee.objects.create(
                    first_name=request.data.get('first_name'),
                    last_name=request.data.get('last_name'),
                    username=request.data.get("username"),
                    email=request.data.get("email"),
                    password=request.data.get('password'),
                    phone=request.data.get('phone'),
                )

                url = 'http://127.0.0.1:8000/api/v1/auth/users/'
                myobj = {
                    'username': request.data.get('username'),
                    'email': request.data.get('email'),
                    'password': request.data.get('password')
                }
                print(myobj)
                x = requests.post(url, json=myobj)
                print(x)

                return Response(data={"User": request.data, "status": status.HTTP_200_OK})
            except Exception as e:
                res = {"msg": str(e), "data": None, "success": False}
                return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        else:
            res = {"msg": "Invalid data", "data": serializer.errors, "success": False}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    def post(self, request, **kwargs):
        try:
            user = Employee.objects.get(username=request.data["username"])
            if user:
                try:
                    url = 'http://127.0.0.1:8000/api/v1/token/'
                    myobj = {
                        'username': request.data['username'],
                        'password': request.data['password']
                    }
                    x = requests.post(url, json=myobj)
                    print(x)
                    if x.status_code == 200:
                        res = {
                            "msg": "Login successful!",
                            "data": x.json(),
                            "success": True
                        }
                        return Response(data=res, status=status.HTTP_200_OK)
                    else:
                        res = {
                            "msg": "Login failed.",
                            "data": None,
                            "success": False
                        }
                        return Response(data=res, status=status.HTTP_401_UNAUTHORIZED)

                except Exception as e:
                    res = {
                        "msg": 'Fail sent' + str(e),
                        "data": None,
                        "success": False
                    }
                    return Response(data=res, status=status.HTTP_400_BAD_REQUEST)
        except Employee.DoesNotExist:
            print('User not found')

            res = {
                "msg": "User not found.",
                "data": None,
                "success": False
            }
            return Response(data=res, status=status.HTTP_404_NOT_FOUND)


class LogoutAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh', None)
            access_token = request.data.get('access', None)

            if refresh_token:
                refresh_token_obj = RefreshToken(refresh_token)
                refresh_token_obj.blacklist()

            if access_token:
                access_token_obj = RefreshToken(access_token)
                access_token_obj.blacklist()

            return Response(data={"msg": "Logout successful!", "success": True}, status=status.HTTP_200_OK)
        except Exception as e:
            res = {"msg": str(e), "success": False}
            return Response(data=res, status=status.HTTP_400_BAD_REQUEST)

class RestaurantAPIView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        if not pk:
            restaurant = Restaurant.objects.all()
            view = [self.formatRestoView(s) for s in restaurant]
        else:
            try:
                restaurant = Restaurant.objects.get(pk=pk)
                view = self.formatRestoView(restaurant)
            except:
                return Response({"error": "No restaurant with pk = " + str(pk)})
        return Response({"Restoran": view})

    def formatRestoView(self, restaurant):
        return {
            'id ': restaurant.id,
            'name': restaurant.name,
            'contact': restaurant.contact,
            'address': restaurant.address

        }

    def post(self, request, **kwargs):
        serializer = RestaurantSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response({"Restaurant": request.data})

    def put(self, request, **kwargs):
        pk = kwargs.get("pk", None)
        if not pk:
            return Response({"error": "Method Put not allowed"})
        try:
            instance = Restaurant.objects.get(pk=pk)
            print(instance)
        except:
            return Response({"error": "Object does not exists"})
        serializer = RestaurantSerializer(data=request.data, instance=instance)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'Restaurant': self.formatRestoView(instance)})


class MenuApiView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, **kwargs):
        pk = kwargs.get('pk', None)
        if not pk:
            return Response({"error": "No restaurant with pk = " + str(pk)})
        else:
            date = self.today_date()
            try:
                menu = Menu.objects.get(restaurant=pk, created_by=date)
                r = self.formatMenuView(menu)
                return Response({'menu': r})
            except Menu.DoesNotExist:
                return Response({'Menu': 'None'})

    def today_date(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d')
        return formatted_datetime

    def formatMenuView(self, menu):
        return {
            'id ': menu.id,
            'menu': menu.file,
        }

    def post(self, request, **kwargs):
        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    def put(self, request, **kwargs):
        pk = kwargs.get("pk", None)
        deta = kwargs.get("deta", None)
        if not pk or not deta:
            return Response({"error": "Method Put not allowed"})
        try:
            menu = Menu.objects.get(restaurant=pk, created_by=deta)
        except Menu.DoesNotExist:
            return Response({"error": "Object does not exist"})

        if "created_by" in request.data:
            deta_date = datetime.strptime(request.data["created_by"], "%Y-%m-%d").date()
            request.data["created_by"] = deta_date

        serializer = MenuSerializer(menu, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        print(serializer.instance)
        return Response({'Menu': self.formatMenuView(serializer.instance)})

    def delete(self, request, *args, **kwargs):
        pk = kwargs.get("pk", None)
        deta = kwargs.get("deta", None)
        if not pk or not deta:
            return Response({"error": "Method Delete not allowed"})
        try:
            instance = Menu.objects.get(restaurant=pk, created_by=deta)
            instance.delete()
        except:
            return Response({"error": "Object does not exists"})
        return Response({"post": "delete post " + str(pk)})

class VoteAPIView(APIView):
    permission_classes = (IsAuthenticated,)
    def today_date(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d')
        return formatted_datetime

    def get(self, request, menu_id):
        username = request.user.username

        employee = Employee.objects.get(username=username)
        menu = Menu.objects.get(id=menu_id)

        if Vote.objects.filter(employee=employee, menu__id=menu_id).exists():
            res = {"msg": 'You already voted!', "data": None, "success": False}
            return Response(data=res, status=status.HTTP_200_OK)
        else:
            Vote.objects.create(employee=employee, menu=menu)
            menu.votes += 1
            menu.save()
            votes = Vote.objects.all().values()
            return Response({'votes': votes})


class ResultsAPIView(APIView):
    def today_date(self):
        current_datetime = datetime.now()
        formatted_datetime = current_datetime.strftime('%Y-%m-%d')
        return formatted_datetime

    def get(self, request):
        current_menu = Menu.objects.filter(created_by=self.today_date())

        if len(current_menu) == 0:
            res = {
                "msg": 'Results not found! no menus found for today.',
                "data": None,
                "success": False}
            return Response(data=res, status=status.HTTP_200_OK)

        max_votes = current_menu.aggregate(Max('votes'))['votes__max']
        menus_with_max_votes = current_menu.filter(votes=max_votes)

        if len(menus_with_max_votes) == 1:
            res = {
                "data": [{
                    "restaurant": item.restaurant.name,
                    "address": item.restaurant.address,
                    "contact": item.restaurant.contact,
                    "votes": item.votes} for item in menus_with_max_votes],
                "success": True
            }
            return Response(data=res, status=status.HTTP_200_OK)
        else:
            res = {
                "data": [{
                    "restaurant": item.restaurant.name,
                    "address": item.restaurant.address,
                    "contact": item.restaurant.contact,
                    "votes": item.votes} for item in menus_with_max_votes],
                "success": True
            }
            return Response(data=res, status=status.HTTP_200_OK)
