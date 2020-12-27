# CrudVeryAcademy
# 1. dfgdg
- ## A.  dfdfg
- ## B.  dfdfg
    - ijlk
        - hhb
# ============

- Instalasi Django
    - clone git
    - buat venv
    - Langkah ketika bermasalah dengan privillage ketika aktivasi venv:
        - `Set-ExecutionPolicy Unrestricted -Scope Process`
        - `& d:/TUTORIAL/PYTHON/CrudVeryAcademy/venv/Scripts/Activate.ps1`
    - `pip install django djangorestframework django-cors-headers`
    - Membuat admin 'core'
        - `django-admin startproject core .`
    - Membuat app `'blog'`
        - `python manage.py startapp blog`
    - Membuat app `'blog_api'`
        - `python manage.py startapp blog_api`

- Membuat superuser
    - `python manage.py migrate`
    - `python manage.py createsuperuser`
isi username, email, isi password aris1985

- Menambahkan installed apps
    - Masuk ke folder backendapi>settings.py,
    - pada INSTALLED_APPS tambahkan:
        ```
        'rest_framework',
        'corsheaders',
        'blog_api'
        ```
    - Karena ada perubahan pada settings, maka lakukan migrate: `python manage.py migrate`

- Menjalankan server django
    - `python manage.py runserver`
    - jika berhasil, akan muncul halaman django

- Redirect url bawaan django ke url buatan sendiri

    - Fungsi: melakukan redirect url bawaan django ke urls.py buatan sendiri

    - buka file core>urls.py, code:
        ```
        from django.contrib import admin
        from django.urls import path
        from django.conf.urls import include

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('blog.urls',)),
            path('api/',include('blog_api.urls'))
        ]
        ```
- Membuat urls.py untuk blog dan blog_api
    - Buat blog/urls.py
        - code:
        ```
        from django.urls import path
        from django.views.generic import TemplateView

        app_name = 'blog'

        urlpatterns = [
            path('', TemplateView.as_view(template_name="blog/index.html")),

        ]
        ```
    - Buat blog_api/urls.py
        - code:
        ```
        from django.urls import path
        
        app_name = 'blog_api'

        urlpatterns = [
            pass
        ]
        ```

    - registrasi di settings.py
        - di installed_apps, pastikan ada
        ```
            'blog',
            'blog_api',
        ```
        - 
- Menggunakan Template
    - Membuat dir baru `template/blog/index.html`
    - dipengaruhi path yang ada di blog.urls
    - isi index.html dengan content sederhana
    - registrasi di settings.py
        - di templates>dirs
            ```
            'DIRS': [BASE_DIR / 'templates'],
            ```
    - Jalankan `python manage.py runserver`
    - Jika berhasil, maka localhost akan menampilkan content dari index.html

- Blog/Models.py
    - code:
    ```
    from django.db import models
    from django.contrib.auth.models import User
    from django.utils import timezone

    #Model Category
    class Category(models.Model):
        name = models.CharField(max_length=100)

        def __str__(self):
            return self.name

    #Model Post
    class Post(models.Model):

        class PostObjects(models.Manager):
            def get_queryset(self):
                return super().get_queryset() .filter(status='published')

        options = (
            ('draft', 'Draft'),
            ('published', 'Published'),
        )
        category = models.ForeignKey(
            Category, on_delete=models.PROTECT, default=1)
        title = models.CharField(max_length=250)
        excerpt = models.TextField(null=True)
        content = models.TextField()
        slug = models.SlugField(max_length=250, unique_for_date='published')
        published = models.DateTimeField(default=timezone.now)
        author = models.ForeignKey(
            User, on_delete=models.CASCADE, related_name='blog_posts'
        )
        status = models.CharField(
            max_length=10, choices=options, default='published'
        )
        objects = models.Manager() #default manager
        postobjects = PostObjects() #custom manager

        class Meta:
            ordering = ('-published', )

        def __str__(self):
            return self.title
    ```
    - Hasil query bisa dilihat di sqlite explorer (install add on bila belum ada)

- Blog_api/serializers.py
    - code:
    ```
    from rest_framework import serializers
    from blog.models import Post

    class PostSerializer(serializers.ModelSerializer):
        class Meta:
            model = Post
            fields = ('id', 'title', 'author', 'excerpt', 'content', 'status')
    ```
- Blog_api/views.py
    - code:
    ```
    from rest_framework import generics
    from blog.models import Post
    from .serializers import PostSerializer


    class PostList(generics.ListCreateAPIView):
        queryset = Post.postobjects.all()
        serializer_class = PostSerializer
        pass

    class PostDetail(generics.RetrieveDestroyAPIView):
        pass
    ```
- by pass Blog_api/views.py (PostDetail/PostList)  ke urls.py
    - code:
        ```
        from django.urls import path
        from .views import PostList, PostDetail

        app_name = 'blog_api'

        urlpatterns = [
            path('`<int:pk>`/', PostDetail.as_view(), name='detailcreate'),
            path('', PostList.as_view(), name='listcreate')

        ]
        ```
- Tes koneksi serializer -> views -> urls
    - Fungsi: Mengetes koneksi data di serializer, di tampilkan di view, menggunakan alamat by pass di urls
    - http://127.0.0.1:8000/api/
    - Jika berhasil akan menampilkan form Post List
    - field 'author' mempunyai value winandiaris(superuser)
    - Coba isi seluruh form, lalu post, maka akan menghasilkan error foreign keyconstraint failed
    - permasalahannya adalah ada 2 foreign key di blog/models, yaitu fields 'category' dan 'author'. 'category' default=1, namun format default ini belum dibuat

- menghandle error double foreign key
    - Buka blog/admin.py
    - 
- fdgdfg
