from django.urls import path
from .views import *

urlpatterns = [
    # Superuser login
    path('superuser/login/', SuperuserLoginView.as_view(), name='superuser-login'),

    # User registration
    path('register/', RegistrationView.as_view(), name='register'),

    # User login
    path('login/', LoginView.as_view(), name='login'),

    #profile
    path('profile/<int:pk>/', ProfileView.as_view(), name='profile-detail'),

    # List all users (admin only)
    path('users/', UserListView.as_view(), name='user-list'),

    # CRUD for schemes
    path('schemes/', SchemeListCreateView.as_view(), name='scheme-list-create'),
    path('schemes/<int:pk>/', SchemeUpdateDelete.as_view(), name='scheme-update-delete'),

    # List schemes for users
    path('user/schemes/', UserSchemeListView.as_view(), name='user-scheme-list'),

    # Detail view for individual schemes for users
    path('user/schemes/<int:pk>/', UserSchemeDetailView.as_view(), name='user-scheme-detail'),

    # CRUD for news
    path('news/', NewsListCreateView.as_view(), name='news-list-create'),
    path('news/<int:pk>/', NewsUpdateDelete.as_view(), name='news-update-delete'),

    # List news for users
    path('usernews/', UserNewsListView.as_view(), name='user-news-list'),
    path('usernews/<int:pk>',UserNewsDetailView.as_view()),

    # CRUD for agricultural techniques
    path('agricultural-techniques/', AgriculturalTechniqueListCreateView.as_view(), name='agricultural-technique-list-create'),
    path('agricultural-techniques/<int:pk>/', AgriculturalTechniqueUpdateDelete.as_view(), name='agricultural-technique-update-delete'),

    # List agricultural techniques for users
    path('user/agricultural-techniques/', UserAgriculturalTechniqueListView.as_view(), name='user-agricultural-technique-list'),
    path('techniques/<int:pk>/', AgriculturalTechniqueDetail.as_view(), name='agricultural-technique-detail'),

    path('crops/', CropListCreateView.as_view(), name='crop-list-create'),
    path('crops/<int:pk>/', CropUpdateDelete.as_view(), name='crop-detail'),
    #view crops bu user
    path('usercrops/', CropListAPIView.as_view(), name='crop-list'),
    path('usercrops/<int:pk>/', CropDetailAPIView.as_view(), name='crop-detail'),
    
    path('solutions/', SolutionAPIView.as_view(), name='solution-api'),
    path('solutions/<int:pk>/', SolutionAPIView.as_view(), name='solution-detail'),

    #get solution by user/farmer
    path('get_solution/', SolutionView.as_view(), name='get_solution'),
    
    # path('feedback/', FeedbackCreateView.as_view(), name='feedback-create'),
    
    path('farmer-products/', FarmerProductListCreateView.as_view(), name='farmer_product_list_create'),
    path('farmer-products/<int:pk>/', FarmerProductDetailView.as_view(), name='farmer_product_detail'),
    
    # path('feedback/', FeedbackCreateView.as_view(), name='feedback_create'),
    # path('feedback/<int:pk>/', FeedbackDetailView.as_view(), name='feedback_detail'),
    
    # path('AddToCart/<int:product_id>/<int:quantity>/', AddToCart.as_view(), name='add_to_cart'),
    # path('cart-items/', CartItemsListview.as_view(), name='cart_items_list'),
    # path('cart-item-delete/<int:pk>/', CartItemDelete.as_view(), name='cart_item_delete'),
    
     path('agriculture-offices/', AgricultureOfficeListCreateView.as_view(), name='agriculture_office_list_create'),
    path('agriculture-offices/<int:pk>/', AgricultureOfficeUpdateDelete.as_view(), name='agriculture_office_detail'),
    path('user/agriculture-offices/', UserAgricultureOfficeListView.as_view(), name='user_agriculture_office_list'),
    
     path('farmcart/', FarmCartAPIView.as_view(), name='formcart'),
    path('farm-orders/', FarmOrderCreateAPIView.as_view(), name='farm-order-create'),
    #plant health
    path('health-assessment/', PlantHealthAPIView.as_view(), name='health-assessment'),
    path('health-result/<int:result_id>/', PlantHealthAPIView.as_view(), name='health-result'),
    path('feedback/', FeedbackAPIView.as_view(), name='feedback'),
    path('manipulatefeedback/<int:feedback_id>/', FeedbackUpdateDeleteView.as_view(), name='feedback-detail-api'),

]

