from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import status
from rest_framework import serializers
from .serializers import RegistrationSerializer, LoginSerializer,SchemeSerializer,UserSchemeSerializer,NewsSerializer,AgriculturalTechniqueSerializer,SolutionSerializer,CropSerializer, FeedbackSerializer, FarmerProductSerializer
from .models import CustomUser,SchemeAdd,News, AgriculturalTechnique,Solution,Crop,Feedback,FarmerProduct
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from django.core.exceptions import ObjectDoesNotExist

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
    def get(self, request, *args, **kwargs):
        users = CustomUser.objects.filter(is_superuser=False)
        serializer = RegistrationSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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
        return Response(serializer.data)


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
        return Response(serializer.data)

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

class CropListCreateView(APIView):
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
    

class SolutionListCreateView(APIView):
    def get(self, request):
        solutions = Solution.objects.all()
        serializer = SolutionSerializer(solutions, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = SolutionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SolutionUpdateDeleteView(APIView):
    def get_solution_object(self, pk):
        try:
            return Solution.objects.get(pk=pk)
        except Solution.DoesNotExist:
            return Response({"error": "Solution does not exist"}, status=status.HTTP_404_NOT_FOUND)

    def get(self, request, pk):
        solution = self.get_solution_object(pk)
        serializer = SolutionSerializer(solution)
        return Response(serializer.data)

    def put(self, request, pk):
        solution = self.get_solution_object(pk)
        serializer = SolutionSerializer(instance=solution, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        solution = self.get_solution_object(pk)
        solution.delete()
        return Response({'msg': 'Deleted'})
    
class FeedbackCreateView(APIView):
    def post(self, request):
        serializer = FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request):
        try:
            feedback_instance = Feedback.objects.get(pk=request.data['id'])
        except Feedback.DoesNotExist:
            return Response({"error": "Feedback does not exist"}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = FeedbackSerializer(instance=feedback_instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class FarmerProductListCreateView(APIView):
    def get(self, request):
        farmer_products = FarmerProduct.objects.all()
        serializer = FarmerProductSerializer(farmer_products, many=True)
        return Response(serializer.data)

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
        return Response(serializer.data)

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