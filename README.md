**-----------Django Setup Steps---------**

1. Clone the repository
 
   git clone https://github.com/shweta-bajirao-bamane/machine_test_python_nimap.git

   and open folder

3. Create a Virtual Environment
   python -m venv .venv
   
4. Activate it
  .venv\Scripts\Activate
   
5. Install django
   python -m pip install django

6. cd machine_test
7. pip install django-environ
8. pip install djangorestframework
9. pip install mysqlclient
10. py manage.py runserver 0.0.0.0:8001
    
**----------Project Setup-----------**

1. pythom -m dgango startproject machine_test
2. cd machine_test
3. python manage.py startapp account
4. python manage.py makemigrations
5. python manage.py migrate
6. py manage.py runserver 0.0.0.0:8001

I have not implemented authentication in this project, so I am passing the created_by field through the input request.

**------------This is the Postman API link---------**

https://www.postman.com/prushal/nimap/documentation/z0ng6fh/nimap


