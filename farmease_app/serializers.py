from rest_framework import serializers
from .models import *
from django.contrib.auth import authenticate, login 



class SuperuserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    
    
class RegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'user_type', 'phone', 'address', 'location', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user_type = validated_data.get('user_type', 'User')
        user = CustomUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            user_type=user_type,  
            phone=validated_data['phone'],
            address=validated_data['address'],
            location=validated_data['location']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if not user:
                raise serializers.ValidationError("Invalid credentials")

        else:
            raise serializers.ValidationError("Both username and password are required")

        return data
    
class SchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeAdd
        fields = '__all__'
        
class UserSchemeSerializer(serializers.ModelSerializer):
    class Meta:
        model = SchemeAdd
        fields = ['id','scheme_name', 'start_age', 'end_age', 'description', 'link']

        
class NewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        
        
class AgriculturalTechniqueSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgriculturalTechnique
        fields = ['id', 'title', 'description', 'image']

class CropSerializer(serializers.ModelSerializer):
    techniques = serializers.SlugRelatedField(
        many=True,
        read_only=False,
        queryset=AgriculturalTechnique.objects.all(),
        slug_field='title'
    )

    class Meta:
        model = Crop
        fields = ['id', 'name', 'description', 'climate', 'growth_period', 'harvesting_time', 'techniques']
        

    
class AgricultureOfficeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AgricultureOffice
        fields = ['id', 'name', 'location', 'contact_number', 'email']   

import json

# serializers.py
from rest_framework import serializers
from .models import Solution

class SolutionSerializer(serializers.ModelSerializer):
    solution = serializers.ListField(child=serializers.CharField())

    class Meta:
        model = Solution
        fields = ['id', 'symptoms', 'solution', 'description']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # Convert the newline-separated string to a list for serialization
        representation['solution'] = instance.solution.split('\n')
        return representation

    def create(self, validated_data):
        solution_list = validated_data.pop('solution', [])
        instance = super().create(validated_data)
        instance.solution = "\n".join(solution_list)
        instance.save()
        return instance

    def update(self, instance, validated_data):
        solution_list = validated_data.pop('solution', [])
        instance = super().update(instance, validated_data)
        instance.solution = "\n".join(solution_list)
        instance.save()

        return instance

class SymptomSearchSerializer(serializers.Serializer):
    symptom = serializers.CharField(max_length=255)

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'solution', 'user', 'content', 'date_posted']
        
        
class FarmerProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmerProduct
        fields = '__all__'
        
class FarmCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = FarmCart
        fields = '__all__'


class FarmOrderSerializer(serializers.ModelSerializer):
    crop_details = serializers.SerializerMethodField()

    class Meta:
        model = FarmOrder
        fields = '__all__'

    def get_crop_details(self, instance):
        crop_names = instance.crop_names
        quantities = instance.quantities
        prices = instance.prices

        if crop_names is None or quantities is None or prices is None:
            return []

        crop_names = crop_names.strip('[]').split(', ')
        quantities = quantities.strip('[]').split(', ')
        prices = prices.strip('[]').split(', ')

        crop_details = []

        for name, quantity, price in zip(crop_names, quantities, prices):
            crop_details.append({
                "name": name.strip("'"),
                "quantity": quantity.strip("' "),
                "price": price.strip("' "),
            })

        return crop_details

    def to_representation(self, instance):
        representation = super().to_representation(instance)

        representation.pop('crop_names', None)
        representation.pop('quantities', None)
        representation.pop('prices', None)

        response_data = {
            "status": 1,
            "data": representation
        }
        if instance.status == 'cancelled':
            response_data["status"] = 0
        return response_data
    
        
        
# class CartItemSerializer(serializers.ModelSerializer):
#     productname = serializers.CharField(source='product.name', read_only=True)
#     price = serializers.DecimalField(source='product.price',decimal_places=2, max_digits=10, read_only=True)
#     user = serializers.CharField(source='cart.user', read_only=True)
#     user_id = serializers.IntegerField(source='cart.user.id', read_only=True)
#     total_price = serializers.DecimalField(source='cart.total_price',decimal_places=2, max_digits=10, read_only=True)
#     class Meta:
#         model = CartItem
#         fields = ['id', 'cart', 'productname', 'quantity','user','total_price','price','user_id']

# class CartItemDeleteSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = CartItem
#         fields = '__all__'
        
# class AgricultureOfficeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = AgricultureOffice
#         fields = ['id', 'name', 'location', 'contact_number', 'email']
        
        
# class FarmOrderSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = FarmOrder
#         fields = '__all__'