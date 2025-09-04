**-----------Django Setup Steps---------**

1. Clone the repository
 
   git clone https://github.com/shweta-bajirao-bamane/machine_test_python_nimap.git

2. Create a Virtual Environment
   python -m venv .venv
   
4. Activate it
  .venv\Scripts\Activate
   
6. Install django
   python -m pip install django

**----------Project Setup-----------**

1. pythom -m dgango startproject machine_test
2. cd machine_test
3. python manage.py startapp account
4. python manage.py makemigrations
5. python manage.py migrate

I have not implemented authentication in this project, so I am passing the created_by field through the input request.

**------------This is the Postman API link---------**

https://www.postman.com/prushal/nimap/documentation/z0ng6fh/nimap


