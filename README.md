# Blog Project - Django Rest Framework

## Instalasi
- set workspace
    - clone project dari github
    - cd crudveryacademy
    - python -m venv venv
    - source venv/bin/activate
- Install dependensi
    - pip install django
    - pip install -r requirements.txt --> pastikan semua aplikasi berhasil terinstall. lakukan manual jika ada yang gagal
    - pip freeze > requirements.txt (optional)
    - python manage.py migrate
- Membuat user admin
    - python manage.py createsuperuser
- Run apps
    - python manage.py runserver
    - 127.0.0.1:8000/api/
    - Isi data : 

## Module
- Django 4
- django rest framework

## Project - apps
- core
    - blog
    - blog_api
## Docs
- core
    - settings.py
        - registrasi apps dan module
        - setting rest framework permission
        - setting cors allowed url
    - urls.py
        - admin/
        - '' --> blog.urls
        - api/ --> blog_api.urls
        - api-auth/ --> rest_framework.urls (ndak ada folder apps-nya)
- blog
    - Note : 
        - blog disini hanya sebagai testing api sebelum menggunakan react di step selanjutnya.
        - blog lebih berperan menyediakan model untuk nanti dikonsumsi serializer di blog_api
        - templates > index.html disini hanya dummy, kosong
        - No views, views nanti secara fungsional ada di blog_api
    - models.py
        - Category()
        - Post()
            - PostObjects() --> sebagai class custom model manager, super()
            - options, category, title, dll.
            - postobjects = PostObjects() --> set PostObject() sebagai custom manager
    - urls.py
        - '' --> TemplateView.as_view --> index.html
    - templates --> index.html

- blog_api
    - NOTE:
        - serializer mengambil dari models.blog
        - views.py mengolah serializer
    - serializers.py
        - PostSerializers()
            - model, fields
    - views.py
        - PostUserWritePermission()
        - PostList()
        - PostDetail()
