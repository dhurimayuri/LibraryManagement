from rest_framework import status, generics
from rest_framework.response import Response
from .models import Book
from rest_framework.views import APIView
from django.contrib.auth import authenticate
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from .serializers import BookSerializer, UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from django.shortcuts import render


def home(request):
    return render(request, 'book.html')

# User Creation View (Admin Signup)
class UserCreateView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        # Extract data from the request
        data = request.data
        username = data.get('username')
        email = data.get('email')

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists. Please choose a different one.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists. Please use a different email.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Proceed with creating the user if not existing
        # Create the user and generate a token
        response = super().post(request, *args, **kwargs)
        user = User.objects.get(email=email)
        token, created = Token.objects.get_or_create(user=user)
        
        return Response({'message': 'Admin registered successfully', 'token': token.key},
                        status=status.HTTP_201_CREATED)

class CustomLoginView(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        # Deserialize the request data using the LoginSerializer
        serializer = LoginSerializer(data=request.data)
        
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            # Retrieve user by email
            try:
                user = User.objects.get(email=email)
            except User.DoesNotExist:
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

            # Authenticate using username
            user = authenticate(username=user.username, password=password)
            # Authenticate the user
            #user = authenticate(username=email, password=password)
            
            if user is not None:
                # Authentication successful
                token, created = Token.objects.get_or_create(user=user)
                return Response( {'token': token.key}, status=status.HTTP_200_OK)
            else:
                # Invalid credentials
                return Response({'message': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)
# Book Create View (Admin can add a new book)
class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if user is authenticated and staff
        if not request.user.is_authenticated:
            return Response({"detail": "Authentication credentials were not provided."}, status=401)
        
        if not request.user.is_staff:
            return Response({"detail": "You don't have permission to perform this action."}, status=403)
        print(f"Authenticated user: {request.user.username}")
        serializer = BookSerializer(data=request.data)
        
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "Book created successfully."}, status=201)
        return Response(serializer.errors, status=400)

# Book List View (Student can view all books)
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]

# Book Update View (Admin can update a book)
class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        if not self.request.user.is_staff:
            raise PermissionDenied("Only admins can update books.")
        serializer.save()

# Book Delete View (Admin can delete a book)
class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        book_id = kwargs.get("pk")  # Get book ID from URL
        try:
            book = Book.objects.get(pk=book_id)
            if not request.user.is_staff:
                raise PermissionDenied("Only admins can delete books.")
            
            book.delete()
            return Response({"message": "Book deleted successfully"}, status=status.HTTP_200_OK)

        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

