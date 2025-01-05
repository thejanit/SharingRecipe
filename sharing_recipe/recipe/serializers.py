from recipe.models import Recipe, Comment, Rating, Categories, UserProfile
from rest_framework import serializers
from django.contrib.auth.models import User


class RecipeSerializer(serializers.ModelSerializer):
    category_name = serializers.PrimaryKeyRelatedField(
        queryset=Categories.objects.all(),
        write_only=True
    )
    category_name_show = serializers.StringRelatedField(source='category_name', read_only=True)
    
    class Meta:
        model = Recipe
        fields = ['id', 'title', 'ingredients', 'instructions', 'image', 'category_name', 'category_name_show']


class CommentSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True
    )

    class Meta:
        model = Comment
        fields = ['id', 'recipe', 'user', 'text', 'created_at']
        read_only_fields = ['user', 'created_at']


class RatingSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)
    recipe = serializers.PrimaryKeyRelatedField(
        queryset=Recipe.objects.all(),
        write_only=True
    )
    
    class Meta:
        model = Rating
        fields = ['id', 'recipe', 'user', 'score']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()
        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Categories
        fields = ['id', 'category_name']


class UserProfileSerializer(serializers.ModelSerializer):
    serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = UserProfile
        fields = ['user', 'bio', 'profile_picture', 'favorite_recipes']