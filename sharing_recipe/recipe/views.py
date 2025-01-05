from django.shortcuts import render
from rest_framework import viewsets, permissions
from recipe.models import Recipe, Comment, Rating, Categories, UserProfile
from recipe.serializers import RecipeSerializer, CommentSerializer, RatingSerializer, UserSerializer, CategorySerializer, UserProfileSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status, serializers
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        # Save the user who created the recipe
        serializer.save(user=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter comments by recipe ID, if present
        recipe_id = self.request.query_params.get('recipe', None)
        if recipe_id:
            return Comment.objects.filter(recipe=recipe_id)
        return Comment.objects.all()

    def perform_create(self, serializer):
        # Ensure a user can comment on a recipe only once
        if Comment.objects.filter(recipe=serializer.validated_data['recipe'], user=self.request.user).exists():
            raise serializers.ValidationError("You have already commented on this recipe.")
        serializer.save(user=self.request.user)


class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Filter ratings by recipe ID, if present
        recipe_id = self.request.query_params.get('recipe', None)
        if recipe_id:
            return Rating.objects.filter(recipe=recipe_id)
        return Rating.objects.all()

    def perform_create(self, serializer):
        # Ensure a user can rate a recipe only once
        if Rating.objects.filter(recipe=serializer.validated_data['recipe'], user=self.request.user).exists():
            raise serializers.ValidationError("You have already rated this recipe.")
        serializer.save(user=self.request.user)


class UserRegistration(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Register new user
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLogin(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        # Handle user login and return a JWT token
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                "message": "Login successful",
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh)
            }, status=status.HTTP_200_OK)
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)


class GetCategory(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, *args, **kwargs):
        categories = Categories.objects.all()
        serialized_categories = CategorySerializer(categories, many=True)
        return Response(serialized_categories.data, status=200)


class Profile(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        user_profile = UserProfile.objects.get(user=request.user)
        serialized_profile = UserProfileSerializer(user_profile)
        return Response(serialized_profile.data)
    
    def put(self, request):
        profile = UserProfile.objects.get(user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)