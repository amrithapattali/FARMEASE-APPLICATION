from django.shortcuts import render

# Create your views here.
from rest_framework import generics
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework import serializers
from .serializers import *
from .serializers import AgricultureOfficeSerializer
from .models import  *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from django.core.exceptions import ObjectDoesNotExist

# import razorpay
from django.db import transaction
from django.conf import settings
from django.http import JsonResponse
from datetime import datetime, timedelta
from django.utils import timezone

class SuperuserLoginView(APIView):
    permission_classes = [AllowAny]
   

    @method_decorator(csrf_exempt)
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        if not username or not password:
            return Response({'error': 'Both username and password are required'}, status=status.HTTP_400_BAD_REQUEST)

        user = authenticate(request, username=username, password=password)

        if user and user.is_superuser:
            login(request, user)

            # Using Django's Token model to generate a normal token
            token, created = Token.objects.get_or_create(user=user)

            # Include superuser details and token in the response
            superuser_data = {
                'id': user.id,
                'username': user.username,
                'email': user.email,
            }

            return Response({'token': token.key, 'superuser': superuser_data, 'message': "Logged in successfully"}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials or user is not a superuser'}, status=status.HTTP_401_UNAUTHORIZED)


class RegistrationView(APIView):
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({'msg': 'Registration successful'}, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    def get(self,request):
        qs=CustomUser.objects.all()
        
        a=RegistrationSerializer(qs,many=True)
        
        return Response(a.data)


#login for farmer and user
    

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']

            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                token, created = Token.objects.get_or_create(user=user)

                # Include user details in the response
                user_data = {
                    'username': user.username,
                    'email': user.email,
                    'user_type': user.user_type,  # Assuming user_type is a field in your CustomUser model
                    'phone': user.phone,
                    'address': user.address,
                    'location': user.location,
                }

                return Response({'token': token.key, 'user': user_data, 'msg': 'Login successful'}, status=200)
            else:
                return Response({'msg': 'Invalid credentials'}, status=401)
        else:
            return Response(serializer.errors, status=400)
        

#admin view all the user /farmer details
    
class UserListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.filter(is_superuser=False)
        serializer = RegistrationSerializer(users, many=True)
        if serializer.data:
            return Response({"status":1,"data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"status":0,"Message":"No Purchases"},status=status.HTTP_200_OK)
#Scheme add by admin
        
class SchemeListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Attempt to retrieve the super admin user based on superuser status
        try:
            super_admin = CustomUser.objects.get(is_superuser=True)
        except ObjectDoesNotExist:
            # Handle the case where the super admin user does not exist
            return Response({"error": "Super admin user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Set the created_by field to the super admin user ID
        mutable_data['created_by'] = super_admin.id

        serializer = SchemeSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        qs = SchemeAdd.objects.all()
        serializer = SchemeSerializer(qs, many=True)
        return Response(serializer.data)
    

#scheme update by admin
class SchemeUpdateDelete(APIView):
    
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def get(self,request,**kwargs):
        scheme=SchemeAdd.objects.get(id=kwargs.get('pk'))
        a=SchemeSerializer(scheme)
        return Response(a.data)
    def put(self,request,**kwargs):
        scheme=SchemeAdd.objects.get(id=kwargs.get('pk'))
        a=SchemeSerializer(instance=scheme,data=request.data)
        if a.is_valid():
            a.save()
        return Response(a.data)
    def delete(self,request,**kwargs):
        scheme=SchemeAdd.objects.get(id=kwargs.get('pk'))
        scheme.delete()
        return Response({'msg': 'Deleted'})
    
#Scheme view by User/Farmer
        
class UserSchemeListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        qs = SchemeAdd.objects.all()
        serializer = UserSchemeSerializer(qs, many=True)
        return Response(serializer.data)
    

#view specific schema
    
class UserSchemeDetailView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            scheme = SchemeAdd.objects.get(id=pk)
        except SchemeAdd.DoesNotExist:
            return Response({"error": "Scheme not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = UserSchemeSerializer(scheme)
        return Response(serializer.data)
    
 
 #News add by admin
    
class NewsListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        # Attempt to retrieve the super admin user based on superuser status
        try:
            super_admin = CustomUser.objects.get(is_superuser=True)
        except ObjectDoesNotExist:
            # Handle the case where the super admin user does not exist
            return Response({"error": "Super admin user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        # Create a mutable copy of the request data
        mutable_data = request.data.copy()

        # Set the created_by field to the super admin user ID
        mutable_data['created_by'] = super_admin.id

        serializer = NewsSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)
    
#view specific news by user

class UserNewsDetailView(APIView):
   

    def get(self, request, pk):
        try:
            news = News.objects.get(id=pk)
        except News.DoesNotExist:
            return Response({"error": "Scheme not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = NewsSerializer(news)
        return Response({'status':1,'data':serializer.data})    

#News update by admin

class NewsUpdateDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_news_object(self, pk):
        try:
            return News.objects.get(pk=pk)
        except News.DoesNotExist:
            return Response({"error": "News does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        news = self.get_news_object(pk)
        serializer = NewsSerializer(news)
        return Response(serializer.data)

    def put(self, request, pk):
        news = self.get_news_object(pk)
        serializer = NewsSerializer(instance=news, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        news = self.get_news_object(pk)
        news.delete()
        return Response({'msg': 'Deleted'})
    

# News view by User/Farmer

class UserNewsListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        news = News.objects.all()
        serializer = NewsSerializer(news, many=True)
        return Response(serializer.data)
    
 #AgricultureOffice add by admin   
    
class AgricultureOfficeListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            super_admin = CustomUser.objects.get(is_superuser=True)
        except ObjectDoesNotExist:
            return Response({"error": "Super admin user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        mutable_data = request.data.copy()
        mutable_data['created_by'] = super_admin.id

        serializer = AgricultureOfficeSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        agriculture_offices = AgricultureOffice.objects.all()
        serializer = AgricultureOfficeSerializer(agriculture_offices, many=True)
        if serializer.data:
            return Response({"status":1,"data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"status":0,"Message":"No agriculture office"},status=status.HTTP_204_NO_CONTENT)

class AgricultureOfficeUpdateDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_agriculture_office_object(self, pk):
        try:
            return AgricultureOffice.objects.get(pk=pk)
        except AgricultureOffice.DoesNotExist:
            return Response({"error": "Agriculture office does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        agriculture_office = self.get_agriculture_office_object(pk)
        serializer = AgricultureOfficeSerializer(agriculture_office)
        if serializer.data:
            return Response({"status":1,"data":serializer.data},status=status.HTTP_200_OK)
        else:
            return Response({"status":0,"Message":"No agriculture office"},status=status.HTTP_204_NO_CONTENT)
    
    def put(self, request, pk):
        agriculture_office = self.get_agriculture_office_object(pk)
        serializer = AgricultureOfficeSerializer(instance=agriculture_office, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        agriculture_office = self.get_agriculture_office_object(pk)
        agriculture_office.delete()
        return Response({'msg': 'Deleted'})
    
    
#Agriculturaloffice  view by User/Farmer

class UserAgricultureOfficeListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        agriculture_offices = AgricultureOffice.objects.all()
        serializer = AgricultureOfficeSerializer(agriculture_offices, many=True)
        return Response(serializer.data)
 
 #AgriculturalTechnique add by admin   
    
class AgriculturalTechniqueListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def post(self, request):
        try:
            super_admin = CustomUser.objects.get(is_superuser=True)
        except ObjectDoesNotExist:
            return Response({"error": "Super admin user does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        mutable_data = request.data.copy()
        mutable_data['created_by'] = super_admin.id

        serializer = AgriculturalTechniqueSerializer(data=mutable_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        techniques = AgriculturalTechnique.objects.all()
        serializer = AgriculturalTechniqueSerializer(techniques, many=True)
        if serializer.data:
                return Response({"status":1,"data":serializer.data},status=status.HTTP_200_OK)
        else:
                return Response({"status":0,"Message":"No product"},status=status.HTTP_204_NO_CONTENT)


class AgriculturalTechniqueUpdateDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_technique_object(self, pk):
        try:
            return AgriculturalTechnique.objects.get(pk=pk)
        except AgriculturalTechnique.DoesNotExist:
            return Response({"error": "Agricultural technique does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        technique = self.get_technique_object(pk)
        serializer = AgriculturalTechniqueSerializer(technique)
        if serializer.data:
                return Response({"status":1,"data":serializer.data},status=status.HTTP_200_OK)
        else:
                return Response({"status":0,"Message":"No product"},status=status.HTTP_204_NO_CONTENT)
    def put(self, request, pk):
        technique = self.get_technique_object(pk)
        serializer = AgriculturalTechniqueSerializer(instance=technique, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        technique = self.get_technique_object(pk)
        technique.delete()
        return Response({'msg': 'Deleted'})
    
class UserAgriculturalTechniqueListView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        techniques = AgriculturalTechnique.objects.all()
        serializer = AgriculturalTechniqueSerializer(techniques, many=True)
        return Response(serializer.data)
    
#Crop add by admin 

class CropListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request):
        crops = Crop.objects.all()
        serializer = CropSerializer(crops, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = CropSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CropUpdateDelete(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]

    def get_crop_object(self, pk):
        try:
            return Crop.objects.get(pk=pk)
        except Crop.DoesNotExist:
            return Response({"error": "Crop does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        crop = self.get_crop_object(pk)
        serializer = CropSerializer(crop)
        return Response(serializer.data)

    def put(self, request, pk):
        crop = self.get_crop_object(pk)
        serializer = CropSerializer(instance=crop, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        crop = self.get_crop_object(pk)
        crop.delete()
        return Response({'msg': 'Deleted'})
    
#solution add by admin 
from django.http import Http404


    
class SolutionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def get(self, request, *args, **kwargs):
        solutions = Solution.objects.all()
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class SolutionAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAdminUser]
    def get(self, request, pk=None, *args, **kwargs):
        # Retrieve a single solution or all solutions
        if pk:
            solution = self.get_object(pk)
            serializer = SolutionSerializer(solution)
        else:
            solutions = Solution.objects.all()
            serializer = SolutionSerializer(solutions, many=True)

        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        # Create a new solution
        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk, *args, **kwargs):
        print(request.data)  # Add this line to inspect the request data
        solution = self.get_object(pk)
        serializer = SolutionSerializer(solution, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            print(serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, *args, **kwargs):
        # Delete an existing solution
        solution = self.get_object(pk)
        solution.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def get_object(self, pk):
        # Helper method to get a Solution instance by primary key
        try:
            return Solution.objects.get(pk=pk)
        except Solution.DoesNotExist:
            raise Http404


class SolutionView(APIView):
    def get(self, request):
        symptom = request.query_params.get('symptom', '')

        try:
            solution = Solution.objects.get(symptoms__icontains=symptom)
            serializer = SolutionSerializer(solution)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Solution.DoesNotExist:
            return Response({'detail': 'Symptom not found'}, status=status.HTTP_404_NOT_FOUND)

    # You can add the following logic to handle symptom searches using a POST request
    def post(self, request):
        serializer = SymptomSearchSerializer(data=request.data)

        if serializer.is_valid():
            symptom = serializer.validated_data['symptom']

            try:
                solution = Solution.objects.get(symptoms__icontains=symptom)
                serializer = SolutionSerializer(solution)
                return Response(serializer.data, status=status.HTTP_200_OK)

            except Solution.DoesNotExist:
                return Response({'detail': 'Symptom not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
       
    
# class FeedbackCreateView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def post(self, request):
#         serializer = FeedbackSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(user=request.user)  # Assign the current user to the 'user' field
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# class FeedbackDetailView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get_feedback_object(self, pk):
#         try:
#             return Feedback.objects.get(pk=pk)
#         except Feedback.DoesNotExist:
#             return Response({"error": "Feedback does not exist"}, status=status.HTTP_404_NOT_FOUND)

#     def get(self, request, pk):
#         feedback = self.get_feedback_object(pk)
#         serializer = FeedbackSerializer(feedback)
#         return Response(serializer.data)

#     def put(self, request, pk):
#         feedback = self.get_feedback_object(pk)
#         serializer = FeedbackSerializer(instance=feedback, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     def delete(self, request, pk):
#         feedback = self.get_feedback_object(pk)
#         feedback.delete()
#         return Response({'msg': 'Deleted'})
    
    
class FarmerProductListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request):
        farmer_products = FarmerProduct.objects.all()
        serializer = FarmerProductSerializer(farmer_products, many=True)
        if serializer.data:
                return Response({"status":1,"data":serializer.data},status=status.HTTP_200_OK)
        else:
                return Response({"status":0,"Message":"No product"},status=status.HTTP_204_NO_CONTENT)
   
    def post(self, request):
        serializer = FarmerProductSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(posted_by=request.user)  # Assign the posted_by to the current user
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FarmerProductDetailView(APIView):
    def get_farmer_product_object(self, pk):
        try:
            return FarmerProduct.objects.get(pk=pk)
        except FarmerProduct.DoesNotExist:
            return Response({"error": "FarmerProduct does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        farmer_product = self.get_farmer_product_object(pk)
        serializer = FarmerProductSerializer(farmer_product)
        if serializer.data:
                return Response({"status":1,"data":serializer.data},status=status.HTTP_200_OK)
        else:
                return Response({"status":0,"Message":"No product"},status=status.HTTP_204_NO_CONTENT)
        
    def put(self, request, pk):
        farmer_product = self.get_farmer_product_object(pk)
        serializer = FarmerProductSerializer(instance=farmer_product, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        farmer_product = self.get_farmer_product_object(pk)
        farmer_product.delete()
        return Response({'msg': 'Deleted'})
    
class FarmCartAPIView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            crop_name = request.data.get('crop_name')
            quantity = int(request.data.get('quantity', 1))

            farm_product = FarmerProduct.objects.get(crop_name=crop_name)

            # Check if the item is already in the cart for the specific user
            cart_item, created = FarmCart.objects.get_or_create(
                user=user,
                crop_name=farm_product.crop_name,
                defaults={
                    'posted_by': farm_product.posted_by.username,
                    'image': farm_product.image,
                    'price': farm_product.price,
                    'quantity': 0,  # Set initial quantity to 0
                    'description': farm_product.description,
                }
            )

            # If quantity is negative, decrement the quantity
            if quantity < 0:
                if cart_item.quantity + quantity <= 0:
                    # If quantity becomes non-positive, remove the item from the cart
                    cart_item.delete()
                else:
                    # Update quantity and price
                    cart_item.quantity += quantity
                    cart_item.price = farm_product.price * cart_item.quantity
                    cart_item.save()
            else:
                # Update quantity and price for positive quantity
                cart_item.quantity += quantity
                cart_item.price = farm_product.price * cart_item.quantity
                cart_item.save()

            # Get all cart items
            cart_items = FarmCart.objects.filter(user=user)

            # Create a list of items with names and quantities
            items_list = [{'name': item.crop_name, 'quantity': item.quantity} for item in cart_items]

            # Calculate total sum of prices in the cart
            total_price = sum(item.price for item in cart_items)
            total_quantity_bought = sum(item.quantity for item in cart_items)

            response_data = {
                'status': 1,  # Status 1 indicates success
                'message': 'Item added to cart successfully.',
                'items': items_list,
                'total_price': total_price,
                'total_quantity_bought': total_quantity_bought
            }

            return Response(response_data, status=status.HTTP_201_CREATED)

        except FarmerProduct.DoesNotExist:
            response_data = {'status': 0, 'error': 'FarmProduct not found.'}
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            response_data = {'status': 0, 'error': str(e)}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            cart_items = FarmCart.objects.filter(user=user)

            # Create a list of items with names, quantities, and additional details
            items_list = [
                {
                    'name': item.crop_name,
                    'posted_by': item.posted_by,
                    'image': str(item.image),
                    'price': item.price,
                    'quantity': item.quantity,
                    'description': item.description,
                }
                for item in cart_items
            ]

            # Calculate total sum of prices in the cart
            total_price = sum(item.price for item in cart_items)
            total_quantity_bought = sum(item.quantity for item in cart_items)

            response_data = {
                'status': 1,  # Status 1 indicates success
                'items': items_list,
                'total_price': total_price,
                'total_quantity_bought': total_quantity_bought
            }

            return Response(response_data, status=status.HTTP_200_OK)

        except Exception as e:
            response_data = {'status': 0, 'error': str(e)}
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        




class FarmOrderCreateAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        try:
            user = request.user
            farm_orders = FarmOrder.objects.filter(username=user)

            serializer = FarmOrderSerializer(farm_orders, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, *args, **kwargs):
        try:
            with transaction.atomic():
                user = request.user
                address = request.data.get('address', '')
                cart_items = FarmCart.objects.filter(user=user)

                crop_names = []
                quantities = []
                prices = []
                total_price = 0.0

                for cart_item in cart_items:
                    crop_names.append(cart_item.crop_name)
                    quantities.append(cart_item.quantity)
                    prices.append(cart_item.price)
                    total_price += cart_item.price

                order_date = timezone.now()
                estimated_date = (order_date + timedelta(days=10)).date()

                # Convert lists to strings with appropriate format
                crop_names_str = str(crop_names)
                quantities_str = str(quantities)
                prices_str = str(prices)

                farm_order = FarmOrder.objects.create(
                    username=user,
                    address=address,
                    crop_names=crop_names_str,
                    quantities=quantities_str,
                    prices=prices_str,
                    total=total_price,
                    order_date=order_date,
                    estimated_date=estimated_date,
                )

                cart_items.delete()

                farm_order_serializer = FarmOrderSerializer(farm_order)
                farm_order_data = farm_order_serializer.data

                return Response(farm_order_data, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        



# class AddToCart(generics.CreateAPIView):
#     permission_classes =[IsAuthenticated]
#     serializer_class = CartItemSerializer

#     def post(self, request, *args, **kwargs):     
#         user = request.user
#         product_id = self.kwargs.get('product_id')
#         products = get_object_or_404(FarmerProduct, pk=product_id)
#         quantity = self.kwargs.get('quantity')
#         if quantity <= products.quantity:
#             if not product_id:
#                 return Response({'error': 'Product ID is required'}, status=status.HTTP_400_BAD_REQUEST)
#             try:
#                 cart = Cart.objects.get(user=user)
#             except Cart.DoesNotExist:
#                 cart = Cart.objects.create(user=user)
#             product = FarmerProduct.objects.get(pk=product_id)  
#             try:
#                 cart_item = CartItem.objects.get(cart=cart, product=product)
#                 cart_item.quantity += quantity
#                 cart_item.save()
#             except CartItem.DoesNotExist:
#                 cart_item = CartItem.objects.create(cart=cart, product=product, quantity=quantity)

#             serializer = self.get_serializer(cart_item)
#         else:
#             return Response({'error':'That much product not available'}, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# class CartItemsListview(APIView):
#     serializer_class=CartItemSerializer
#     queryset=CartItem.objects.all()
#     permission_classes = [IsAuthenticated]

#     def get(self,request,format=None):
#         try:
#             user=self.request.user
#             query=CartItem.objects.filter(cart__user=user)
#             serializer = self.serializer_class(query, many=True)
#             if serializer.data:
#                 return Response({"status":1,"data":serializer.data},status=status.HTTP_200_OK)
#             else:
#                 return Response({"status":0,"Messtage":"No items in cart"})
#         except:
#             return Response({"Message":"somthing went wrong"})
        
# class CartItemDelete(APIView):
#     serializer_class = CartItemDeleteSerializer
#     permission_classes = [IsAuthenticated]

#     def delete(self, request, pk):
#         try:
#             cart_item = CartItem.objects.get(pk=pk)
#         except CartItem.DoesNotExist:
#             return Response({"error": "Cart item does not exist"}, status=status.HTTP_404_NOT_FOUND)

#         cart_item.delete()
#         return Response({'msg': 'Deleted'}, status=status.HTTP_204_NO_CONTENT)
    
    
# class OrderProductAPIView(APIView):
#     def post(self, request):
#         try:
#             user = request.user
#             address = request.data.get('address', '')
#             cart_items = CartItem.objects.filter(cart__user=user)

#             crop_names = []
#             quantities = []
#             prices = []
#             total_price = 0

#             for cart_item in cart_items:
#                 crop_names.append(cart_item.product)
#                 quantities.append(cart_item.quantity)
#                 prices.append(cart_item.total_price)
#                 total_price += cart_item.total_price

#             order_date = timezone.now()
#             estimated_date = (order_date + timedelta(days=10)).date()

#             farm_order = FarmOrder.objects.create(
#                 username=user,
#                 address=address,
#                 crop_names=crop_names,
#                 quantities=quantities,
#                 prices=prices,
#                 total=total_price,
#                 order_date=order_date,
#                 estimated_date=estimated_date,
#             )

#             cart_items.delete()

#             serializer = FarmOrderSerializer(farm_order)
#             return Response(serializer.data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#             return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# class ViewOrderAPIView(APIView):
#     def get(self, request):
#         try:
#             user = request.user
#             farm_orders = FarmOrder.objects.filter(username=user)
#             serializer = FarmOrderSerializer(farm_orders, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
    
# class FarmOrderCreateAPIView(APIView):
#     authentication_classes = [TokenAuthentication]
#     permission_classes = [IsAuthenticated]

#     def get(self, request, *args, **kwargs):

#         try:
#             user = request.user
#             farm_orders = FarmOrder.objects.filter(username=user)

#             serializer = FarmOrderSerializer(farm_orders, many=True)
#             return Response(serializer.data, status=status.HTTP_200_OK)

#         except Exception as e:
#             return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    
#     def post(self, request, *args, **kwargs):
#         try:
#             with transaction.atomic():
#                 user = request.user
#                 address = request.data.get('address', '')
#                 # Filter cart items based on the user
#                 cart_items = CartItem.objects.filter(cart__user=user)

#                 crop_names = []
#                 quantities = []
#                 prices = []
#                 total_price = 0.0

#             for cart_item in cart_items:
#                 crop_names.append(cart_item.product)
#                 quantities.append(cart_item.quantity)
#                 prices.append(cart_item.total_price )
#                 total_price += cart_item.total_price 

#             order_date = timezone.now()
#             estimated_date = (order_date + timedelta(days=10)).date()

#             # Convert lists to strings with appropriate format
#             crop_names_str = str(crop_names)
#             quantities_str = str(quantities)
#             prices_str = str(prices)

#             farm_order = FarmOrder.objects.create(
#                 username=user,
#                 address=address,
#                 crop_names=crop_names_str,
#                 quantities=quantities_str,
#                 prices=prices_str,
#                 total=total_price,
#                 order_date=order_date,
#                 estimated_date=estimated_date,
#             )

#             cart_items.delete()

#             farm_order_serializer = FarmOrderSerializer(farm_order)
#             farm_order_data = farm_order_serializer.data

#             return Response(farm_order_data, status=status.HTTP_201_CREATED)

#         except Exception as e:
#            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)