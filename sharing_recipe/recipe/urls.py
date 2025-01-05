from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import RecipeViewSet, CommentViewSet, RatingViewSet, UserRegistration, UserLogin, GetCategory, Profile
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'recipes', RecipeViewSet)
router.register(r'comments', CommentViewSet)
router.register(r'ratings', RatingViewSet)

urlpatterns = [
    # User Registration and Login endpoints
    path('register/', UserRegistration.as_view(), name='user-register'),
    path('login/', UserLogin.as_view(), name='user-login'),
    
    # JWT Token endpoints
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Include the router URLs for recipes, comments, and ratings
    path('', include(router.urls)),
    path('categories/', GetCategory.as_view(), name='get-category-list'),
    path('profile/', Profile.as_view(), name='user-profile')
]
