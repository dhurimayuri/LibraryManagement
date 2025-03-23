# urls.py
from django.urls import path
from .views import UserCreateView, BookCreateView, BookListView, BookUpdateView, BookDeleteView, CustomLoginView, LogoutView,home

urlpatterns = [
    path('', home, name='home'),
    path('admin/signup/', UserCreateView.as_view(), name='user-create'),   # Admin signup
    path('admin/login/', CustomLoginView.as_view(), name='admin-login'),  #admin login
    path('admin/book/create/', BookCreateView.as_view(), name='book-create'),  # Create new book
    path('books/', BookListView.as_view(), name='book-list'),  # View all books
    path('admin/book/update/<int:pk>/', BookUpdateView.as_view(), name='book-update'),  # Update a book
    path('admin/book/delete/<int:pk>/', BookDeleteView.as_view(), name='book-delete'),  # Delete a book
    path('admin/logout/',LogoutView.as_view(), name='admin-logout') #admin-logout
]
