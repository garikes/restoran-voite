from rest_framework import serializers
from .models import *


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee
        fields = ['first_name',
                  'last_name',
                  'username',
                  'email',
                  'password',
                  'phone'
                  ]

        def update(self, instance, validated_data):
            instance.first_name = validated_data.get("first_name", instance.first_name)
            instance.last_name = validated_data.get("last_name", instance.contact)
            instance.last_name = validated_data.get("address", instance.address)
            instance.save()
            return instance


class RestaurantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Restaurant
        fields = '__all__'

    def create(self, validated_data):
        return Restaurant.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.name = validated_data.get("name", instance.name)
        instance.contact = validated_data.get("contact", instance.contact)
        instance.address = validated_data.get("address", instance.address)
        instance.save()
        return instance


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = ['restaurant', 'created_by', 'votes', ]

    def create(self, validated_data):
        return Menu.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.restaurant = validated_data.get("restaurant", instance.restaurant)
        instance.file = validated_data.get("file", instance.file)
        instance.created_by = validated_data.get("created_by", instance.created_by)
        instance.votes = validated_data.get("votes", instance.votes)
        instance.save()
        return instance
