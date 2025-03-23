# Library Management System

A Django-based Library Management System where users can view books, and admin users can create, update, and delete books. This system also includes user authentication (with token-based authentication).

## Setup Instructions

Follow these steps to set up the project on your local machine.

### Prerequisites

- Python 3.8 or higher
- MySQL database server
- Django 3.2 or higher

### Installation Steps

1. **Clone the repository:**
   ```
   git clone https://github.com/dhurimayuri/LibraryManagement.git
   ```
   ```
   cd LibraryManagement
    ```
   
2. **Create and activate a virtual environment:**
   
  **For Windows:**
  ``` 
  python -m venv venv
  venv\Scripts\activate
```

  **For macOS/Linux:**
  ```
  python3 -m venv venv
  source venv/bin/activate
```

3. **Install dependencies:**
   
Install the required Python packages using pip:
```
pip install -r requirements.txt
```
4. **Configure MySQL Database:**
   
**Start MySQL Service**

**For Linux/MacOS:**

Open your terminal.
Run the following command to start the MySQL service:
```
sudo service mysql start
```
**For Windows:**

Open Services by typing services.msc in the Run window (Win + R).

Look for MySQL in the list of services.

Right-click on it and select Start.

Update the DATABASES setting in library_management/settings.py to match your MySQL configuration:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'library_management_db',
        'USER': 'your_mysql_username',
        'PASSWORD': 'your_mysql_password',
        'HOST': 'localhost',
        'PORT': '3306',
    }
}
```
Ensure your MySQL server is running.

**Create database using MySQL:**

```
CREATE DATABASE databasename;
```

5. **Apply database migrations:**

Create the necessary tables in your MySQL database:
```
python manage.py migrate
```

6. **Create a superuser:**

To access the Django admin panel, create a superuser:
```
python manage.py createsuperuser
```
7.**Run the development server:**

Start the development server:
```
python manage.py runserver
```
 8. **API ENDPOINTS**
    
 1.Admin User Signup:
```
   POST /api/admin/signup/
```
   Payload:
```
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "adminpassword"
}
```
  2.Admin User Login:
```
  POST /api/admin/login/
```
  Payload:
  ```
  {
  "email": "admin@example.com",
  "password": "adminpassword"
}
```
  3.Book Creation (Admin only):
  ```
  POST /api/admin/book/create/
```
  Payload:
  ```
  {
  "title": "Book Title",
  "author": "Author Name",
  "isbn": "1234567890",
  "published_date": "2025-01-01"
  }
```
  4. Book List (Anyone):
```
  GET /api/books/
```
  Response: A list of all books.

  **View all books from student view**
  ```
http://127.0.0.1:8000/api/home/
```

  5.Book Update (Admin only):
```
  PUT /api/admin/book/update/{book_id}/
```
  Payload:
  ```
  {
  "title": "Updated Book Title",
  "author": "Updated Author Name",
  "isbn": "0987654321",
  "published_date": "2025-02-01"
  }
```
  6.Book Deletion (Admin only):
```
  DELETE /api/admin/book/delete/{book_id}/
```





