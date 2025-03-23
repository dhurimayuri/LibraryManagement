from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, User  # Assuming Book is your model for book entries
from rest_framework.authtoken.models import Token

# User Serializer for Admin Signup and CRUD operations
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'password', 'is_staff']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        # Extract password separately since it's passed as write_only
        password = validated_data.pop('password', None)

        # Ensure the username is set (you could generate one if you want)
        if 'username' not in validated_data:
            validated_data['username'] = validated_data['email']

        # Create user and set them as staff/admin if required
        user = User.objects.create_user(**validated_data)

        # Set the password
        if password:
            user.set_password(password)
            user.save()

        # Ensure user is set as staff/admin
        user.is_staff = True  # Set this to True for admin users
        user.save()

        # Create an associated token for the user
        Token.objects.create(user=user)

        return user

    def update(self, instance, validated_data):
        # Updating the user
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)
        if 'password' in validated_data:
            instance.set_password(validated_data['password'])
        instance.save()
        return instance
class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)
# Book Serializer for CRUD operations on Book model
class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'published_date', 'isbn_number']

    # Create a new Book entry
    def create(self, validated_data):
        book = Book.objects.create(**validated_data)
        return book

    # Update an existing Book entry
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.description = validated_data.get('description', instance.description)
        instance.published_date = validated_data.get('published_date', instance.published_date)
        instance.isbn_number = validated_data.get('isbn_number', instance.isbn_number)
        instance.save()
        return instance

    # Read: This is handled by default through `ModelSerializer` which automatically supports read operations
    # unless you need custom logic for displaying related fields.
