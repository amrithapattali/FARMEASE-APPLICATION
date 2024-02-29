from django.urls import path
from .views import SuperuserLoginView, RegistrationView, LoginView, UserListView, SchemeListCreateView, SchemeUpdateDelete, UserSchemeListView, UserSchemeDetailView, NewsListCreateView, NewsUpdateDelete, UserNewsListView, AgriculturalTechniqueListCreateView, AgriculturalTechniqueUpdateDelete, UserAgriculturalTechniqueListView,CropListCreateView,CropUpdateDelete,SolutionListCreateView,SolutionUpdateDeleteView,FeedbackCreateView,FeedbackDetailView,FarmerProductListCreateView, FarmerProductDetailView,AddToCart, CartItemsListview, CartItemDelete

urlpatterns = [
    # Superuser login
    path('superuser/login/', SuperuserLoginView.as_view(), name='superuser-login'),

    # User registration
    path('register/', RegistrationView.as_view(), name='register'),

    # User login
    path('login/', LoginView.as_view(), name='login'),

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
    path('user/news/', UserNewsListView.as_view(), name='user-news-list'),

    # CRUD for agricultural techniques
    path('agricultural-techniques/', AgriculturalTechniqueListCreateView.as_view(), name='agricultural-technique-list-create'),
    path('agricultural-techniques/<int:pk>/', AgriculturalTechniqueUpdateDelete.as_view(), name='agricultural-technique-update-delete'),

    # List agricultural techniques for users
    path('user/agricultural-techniques/', UserAgriculturalTechniqueListView.as_view(), name='user-agricultural-technique-list'),
    
    path('crops/', CropListCreateView.as_view(), name='crop-list-create'),
    path('crops/<int:pk>/', CropUpdateDelete.as_view(), name='crop-detail'),
    
    path('solutions/', SolutionListCreateView.as_view(), name='solution-list-create'),
    path('solutions/<int:pk>/', SolutionUpdateDeleteView.as_view(), name='solution-update-delete'),
    
    path('feedback/', FeedbackCreateView.as_view(), name='feedback-create'),
    
    path('farmer-products/', FarmerProductListCreateView.as_view(), name='farmer_product_list_create'),
    path('farmer-products/<int:pk>/', FarmerProductDetailView.as_view(), name='farmer_product_detail'),
    
    path('feedback/', FeedbackCreateView.as_view(), name='feedback_create'),
    path('feedback/<int:pk>/', FeedbackDetailView.as_view(), name='feedback_detail'),
    
    path('add-to-cart/<int:product_id>/', AddToCart.as_view(), name='add_to_cart'),
    path('cart-items/', CartItemsListview.as_view(), name='cart_items_list'),
    path('cart-item-delete/<int:pk>/', CartItemDelete.as_view(), name='cart_item_delete'),
]

