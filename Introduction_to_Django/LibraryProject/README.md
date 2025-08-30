# LibraryProject

## 📌 Objective  
The objective of this project is to gain familiarity with **Django** by setting up a Django development environment and creating a basic Django project. This serves as the foundation for future development of Django applications.

---

## 📝 Task Description  
This project walks through:  
- Installing Django  
- Creating a new Django project named **LibraryProject**  
- Running the development server  
- Exploring the project’s default structure  

---

## 🚀 Steps to Run the Project  

### 1. Install Django  
Make sure you have **Python** installed on your system.  
Then, install Django using pip:  

```bash
pip install django
2. Create the Django Project
Run the following command to create a new Django project named LibraryProject:

bash
Copy code
django-admin startproject LibraryProject
3. Run the Development Server
Navigate into your project directory:

bash
Copy code
cd LibraryProject
Start the development server:

bash
Copy code
python manage.py runserver
Now open your browser and go to:

👉 http://127.0.0.1:8000/

You should see the default Django welcome page. 🎉

📂 Project Structure
When you create a new Django project, Django generates several files and folders. Here are the key ones:

manage.py
A command-line utility that lets you interact with your Django project.

LibraryProject/settings.py
Contains all the configuration for the Django project (e.g., database, apps, middleware).

LibraryProject/urls.py
The URL declarations for the project. Think of this as the table of contents for your Django site.

LibraryProject/__init__.py
Marks the directory as a Python package.

LibraryProject/asgi.py & wsgi.py
Entry points for deploying your project using ASGI/WSGI servers.

✅ Next Steps
After completing this setup, you are ready to:

Create Django apps inside the project

Define models, views, and templates

Build out the LibraryProject into a fully functional application