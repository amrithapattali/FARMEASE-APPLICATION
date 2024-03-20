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
    path('news/<int:pk>/', NewsView.as_view(), name='news-retrive'),
    path('newsupdate/<int:pk>/',NewsUpdateView.as_view(),name='newsupdate'),
    path('newsdelete/<int:pk>/',NewsDeleteView.as_view(),name='newsdelete'),

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
    path('crops/<int:pk>/', CropView.as_view(), name='crop-detail'),
    path('cropupdate/<int:pk>/',CropUpdateView.as_view(),name='cropupdate'),
    path('cropdelete/<int:pk>/',CropDeleteView.as_view(),name='cropdelete'),
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
    path('farm-product-update/<int:pk>/',FarmerProductUpdateView.as_view(),name='productupdate'),
    path('farm-product-delete/<int:pk>/',FarmerProductDeleteView.as_view(),name='productdelete'),
    # path('feedback/', FeedbackCreateView.as_view(), name='feedback_create'),
    # path('feedback/<int:pk>/', FeedbackDetailView.as_view(), name='feedback_detail'),
    
    # path('AddToCart/<int:product_id>/<int:quantity>/', AddToCart.as_view(), name='add_to_cart'),
    # path('cart-items/', CartItemsListview.as_view(), name='cart_items_list'),
    # path('cart-item-delete/<int:pk>/', CartItemDelete.as_view(), name='cart_item_delete'),
    
     path('agriculture-offices/', AgricultureOfficeListCreateView.as_view(), name='agriculture_office_list_create'),
    path('agriculture-offices/<int:pk>/', AgricultureOfficeView.as_view(), name='agriculture_office_detail'),
    path('agriofficeupdate/<int:pk>',AgricultureOfficeUpdateView.as_view(),name='agriupdate'),
    path('agridelete/<int:pk>/',AgricultureOfficeDeleteView.as_view(),name='agridelete'),
    path('user/agriculture-offices/', UserAgricultureOfficeListView.as_view(), name='user_agriculture_office_list'),
    
     path('farmcart/', FarmCartAPIView.as_view(), name='formcart'),
    path('farm-orders/', FarmOrderCreateAPIView.as_view(), name='farm-order-create'),
    #plant health
    path('health-assessment/', PlantHealthAPIView.as_view(), name='health-assessment'),
    # path('health-result/<int:result_id>/', PlantHealthAPIView.as_view(), name='health-result'),
    path('feedback/', FeedbackAPIView.as_view(), name='feedback'),
    path('feedback/<int:feedback_id>/', FeedbackView.as_view(), name='feedback-detail-api'),
    path('feedbackupdate/<int:pk>/',HealthFeedbackUpdateView.as_view(),name='feedbackupdate'),
    path('feedbackdelete/<int:pk>/',HealthFeedbackDeleteView.as_view(),name='feedbackdelete'),
    #payment
    path('payments/', PaymentListCreateView.as_view(), name='payment-list-create'),
    path('payments/<int:pk>/',PaymentDetailView.as_view(), name='payment-detail'),
     path('orderfeedback/',OrderFeedbackListAPIView.as_view(), name='orderfeedback-list'),
    path('orderfeedback/<int:pk>/',OrderFeedbackDetailAPIView.as_view(), name='orderfeedback-detail'),
]

