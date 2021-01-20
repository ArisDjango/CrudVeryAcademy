# DAFTAR ISI

- [Heading](#_B._FRONT_END_(REACT))
  * [Sub-heading](#sub-heading)

# A. BASIC_BACKEND-API
## 1. Instalasi
- 1.1. Instalasi Django
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
    - Migrate  `python manage.py migrate`

- 1.2. Membuat superuser
    - `python manage.py createsuperuser`
    - isi username, email, isi password aris1985

- 1.3 Menambahkan installed apps
    - Kita punya 2 app blog_api dan blog yg harus di registrasi
    - Masuk ke folder backendapi>settings.py,
    - pada INSTALLED_APPS tambahkan:
        ```
        'rest_framework',
        'corsheaders',
        'blog_api'
        'blog'
        ```
    - Karena ada perubahan pada settings, maka lakukan migrate: `python manage.py migrate`

- 1.4. Menjalankan server django
    - `python manage.py runserver`
    - jika berhasil, akan muncul halaman django

## 2. Redirect URL
- 2.1. Redirect url bawaan django ke url buatan sendiri
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
- 2.2. Membuat urls.py untuk  __blog__ dan __blog_api__
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
## 3. Template
- Menggunakan Template
    - Membuat dir baru `templates/blog/index.html`
    - dipengaruhi path yang ada di blog.urls
    - isi index.html dengan content sederhana
    - registrasi di settings.py
        - di templates>dirs
            ```
            'DIRS': [BASE_DIR / 'templates'],
            ```
    - Jalankan `python manage.py runserver`
    - Jika berhasil, maka localhost akan menampilkan content dari index.html

## 4. Models
- 4.1. Blog/Models.py
    - Fungsi: Membuat Model database blog
    - Langkah:
        - Import modul model, User(pk), dan timezone
        - class Category (pk)
        - class Post:
            - class postObjects --> queryset
            - var options = draft, published 
            - field category (fk -->class Category)
            - field title, excerpt, content, slug, published
            - field author (fk --> User)
            - var object --> default manager, instantiasi mencakup semua class dan var
            - var postobject --> custom manager
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
            category = models.ForeignKey(Category, on_delete=models.PROTECT,default=1)
            title = models.CharField(max_length=250)
            excerpt = models.TextField(null=True)
            content = models.TextField()
            slug = models.SlugField(max_length=250, unique_for_date='published')
            published = models.DateTimeField(default=timezone.now)
            author = models.ForeignKey(User, on_delete=models.CASCADE,related_name='blog_posts')
            status = models.CharField(max_length=10, choices=options,default='published')
            objects = models.Manager() #default manager
            postobjects = PostObjects() #custom manager

            class Meta:
                ordering = ('-published', )

            def __str__(self):
                return self.title
        ```
    - Hasil query bisa dilihat di sqlite explorer (install add on bila belum ada)

## 5. Blog_api
- 5.1. Blog_api/serializers.py
    - Fungsi: Mengambil data dari model
    - ======================
    - code:
        ```
        from rest_framework import serializers
        from blog.models import Post

        class PostSerializer(serializers.ModelSerializer):
            class Meta:
                model = Post
                fields = ('id', 'title', 'author', 'excerpt', 'content', 'status')


- 5.2. Blog_api/views.py
    - Fungsi:
        - Mengambil data dan menampilkan serializer dalam bentuk form sederhana
        - ListCreateAPIView = menampilkan view api berupa fungsi GET dan POST
        - RetrieveDestroyAPIView = fungsi DELETE dari api (sementara pass, akan dibahas nanti)
    - ===========================
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
- 5.3. Blog_api/urls.py
    - Fungsi: by pass Blog_api/views.py (PostDetail/PostList)  ke urls.py, sehingga bisa diakses melalui http://127.0.0.1:8000/api/
    - Argumen post detail `<int:pk>` = mengambil id(int) dengan primary key yang sedang aktif. Misal: http://127.0.0.1:8000/api/1
    - ================================
    - code:
        ```
        from django.urls import path
        from .views import PostList, PostDetail

        app_name = 'blog_api'

        urlpatterns = [
            path('<int:pk>/', PostDetail.as_view(), name='detailcreate'),
            path('', PostList.as_view(), name='listcreate')

        ]
        
        ```
## 6. model (blog) -> serializers (api) -> Views (api) -> urls (api)

- 6.1. Tes PostList() -> GET dan POST
    - Fungsi: 
        - Mengetes koneksi data dari model diekstrak di serializer, di tampilkan di view, menggunakan alamat by pass dari urls
        - View http://127.0.0.1:8000/api/ akan Menghasilkan tampilan Post list dummy dengan fungsi GET dan POST hasil dari PostList()
    - ========================
       
    - buka http://127.0.0.1:8000/api/
    - Jika berhasil akan menampilkan form Post List dengan tombol GET dibagian atas untuk menampilkan output dan POST dibagian bawah form untuk mengirim form.
    - form field 'author' mempunyai value winandiaris(superuser)
    - Coba isi seluruh form, lalu POST, maka akan menghasilkan error foreign keyconstraint failed
    - permasalahannya adalah ada 2 foreign key di blog/models, yaitu fields 'category' dan 'author'. 'category' default=1, namun format default ini belum dibuat, solusi ada di bab selanjutnya

- 6.2. Menampilkan menu Blog: Posts dan categorys di admin
    - Fungsi:
        - register/menampilkan menu Posts dan categorys di admin panel. Hasil kompilasi input form bisa dilihat disini
        - contoh category bisa di input melalui admin panel, dengan begitu error double foreign key teratasi karena category sudah mempunyai defaults=1

    - ========================
    - Buka blog/admin.py
    - code:
        ```
        from django.contrib import admin
        from . import models

        @admin.register(models.Post)
        class AuthorAdmin(admin.ModelAdmin):
            list_display = ('title', 'id', 'status', 'slug', 'author')
            prepopulated_fields = {'slug': ('title',), }

        admin.site.register(models.Category)
        ```
    - masuk ke http://127.0.0.1:8000/admin
    - Jika berhasil akan muncul menu baru Blog, dengan submenu Categorys dan Post
    - Categorys > Add
    - Buat 1 category, ex:django
    - Maka sekarang category mempunyai defaults=1 yaitu 'django'
    - masuk ke http://127.0.0.1:8000/api/, lalu isi form secara lengkap, jika berhasil akan ditampilkan output json tanpa pesan error
    - Namun sejauh ini belum bisa tampil detail post di view dan serta belum bisa di delete, solusi ada dibawah

- 6.3. Tes PostDetail() -> DELETE:
    - Fungsi: View http://127.0.0.1:8000/api/1 Menghasilkan tampilan Post detail dengan fungsi DELETE Post/category hasil dari PostDetail()
    - =========================
    - Masuk blog_api/views.py/PostDetail()
    - code:
        ```
        class PostDetail(RetrieveDestroyAPIView):
            queryset = Post.objects.all()
            serializer_class = PostSerializer
        ```
    - Jika kita akses http://127.0.0.1:8000/api/1 maka akan muncul detail post
    - Jika kita DELETE, maka post akan hilang

## 7. Unit Testing blog dan blog_api
- 7.1. persiapan testing, Setting permission untuk rest
    - core/settings.py:
    - setting untuk memberikan permission ke semua endpoint
    - code:
        ```
        REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.AllowAny',
            ]
        }
        ```

- 7.2. coverage
    - Fungsi: modul tampilan testing, sehingga mudah di inspeksi
    - Instalasi:
        - `pip install coverage`
        - `coverage run --omit='*venv*' manage.py test`
        - `coverage html`
        - maka akan otomatis membuat htmlcov
        - buka htmlcov/index.html, untuk melihat hasil test dalam bentuk html
        - maka akan muncul halaman test, terlihat mana yang masih missing, yaitu models.py ada 2 missing

- 7.3. Testing blog
    - Langkah testing blog_api:
        - Import unittest dan object yang dibutuhkan
        - Membuat class baru untuk test blog
            - Membuat method untuk `test data`, untuk dummy data
                - var dummy Category --> name:"django"
                - var dummy User --> User/password
                - var dummy Post --> id, title, content,etc...

            - Membuat method test `post blog content`, untuk logic, mengambil dari model
                - var post --> get id=1
                - var category --> get id=1
                - var author s/d content --> dari model
                - Test semua var dengan value= tes data diatas
        - Jika berhasil maka ...
    - ==========================

    - buka blog/test.py
    - code:
        - Import modul test dan beberapa object:
            ```
            from django.test import TestCase
            from django.contrib.auth.models import User
            from blog.models import Post, Category
            ```
        - Membuat class test dan membuat method dummy data
            ```
            class Test_Create_post(TestCase):

            @classmethod
            def setUpTestData(cls): 
                test_category = Category.objects.create(name='django') #dummy category='django'
                testuser1 = User.objects.create_user(username='test_user1', password='123456789') #dummy login username
                test_post = Post.objects.create(category_id=1, title='Post Title', excerpt='Post Excerpt', content='Post Content', slug='post-title', author_id=1, status='published') #dummy posting
                a = Post.objects.
            ```
        - Method blog test
            - variabel Logic, code:
            ```
            def test_blog_content(self): 
                post = Post.postobjects.get(id=1) # mengakses class Post di model, list query utama
                cat = Category.objects.get(id=1) # Mengakses class Category di model
                author = f'{post.author}' # Mengakses data di model
                excerpt = f'{Post.excerpt}'
                title = f'{post.title}'
                content = f'{post.content}'
                status = f'{post.status}'
            ```
            - variabel Unit test, code:
            ```
                self.assertEqual(author, 'test_user1')
                self.assertEqual(title, 'Post Title')
                self.assertEqual(content, 'Post Content')
                self.assertEqual(status, 'published')
                self.assertEqual(str(post), "Post Title")
                self.assertEqual(str(cat), "django")
            ```
        
    - Ulangi proses coverage, lalu buka index.html, jika berhasil maka unit test akan menunjukkan 0 missing
    - jika ada masalah object tidak dikenali, biasanya ada pada linter, untuk itu coba resolve dengan cara:
        - buka setting (tombol kiti bawah)
        - tambahkan:
        ```
            "python.linting.pylintArgs": [
                "--load-plugins",
                "pylint_django",
                "--errors-only",
                "--load-plugins pylint_django"
            ],
        ```

- 7.4. Testing blog_api
    - Langkah testing blog_api:
        - Import unittest dan object yang dibutuhkan
        - Membuat class baru untuk test api
            - Membuat method `test view post`
                - var url reverse --> urls.py
                - var response --> json
                - Test status response http 200
            - Membuat method test `create post test`
                - var dummy data (category dan user)
                - var dummy post
                - var url reverse --> urls.py
                - var response --> json
                - Test status response http 201: past post/get
    - ==============================
    - buka blog_api/test.py
    - code:
        - Import unittest dan object:
        ```
        from django.urls import reverse
        from rest_framework import status
        from rest_framework.test import APITestCase
        from blog.models import Post, Category
        from django.contrib.auth.models import User
        ```
        - Membuat class baru untuk test api:
            - Membuat method `test view post`

                ```
                class PostTest(APITestCase):

                def test_view_post(self):
                    url = reverse('blog_api:listcreate')
                    response = self.client.get(url, format='json') 
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                ```
            - Membuat method test `create post test`:
                - var dummy data (category dan user):
                ```
                def create_post(self):
                    self.test_category = Category.objects.create(name='django')
                    self.test_user1 = User.objects.create_user(username='test_user1', password='123456789')
                ```
                - var dummy post,url reverse, & response:
                ```
                    data = {"title":"new", "author":1, "excerpt":"new", "content":"new"}
                    url = reverse('blog_api:listcreate')
                    response = self.client.post(url, data, format='json')

                ```
                - Test status response http 201: past post/get
                ```
                    self.assertEqual(response.status_code, status.HTTP_201_OK) # koneksi setelah PUT/GET berhasil
                ```

# B. FRONT END (REACT)
ada di file terpisah

# C. PERMISSION DAN CUSTOM PERMISSION
## 1. Default Permission
- 1.1. Pendahuluan
    - Sejauh ini yang kita bangun:
        - Django RestAPI
        - React App yang mengkonsumsi RestAPI
    - Pada bab ini akan membahas sistem permission ketika user mengkases blog_api
    -  https://www.django-rest-framework.org/api-guide/permissions/
    - .

- 1.2. Authentification Url
    - Pada saat mengakses blog_api, perlu halaman login untuk mengotentifikasi user agar ketika masuk mempunyai hak sesuai permission setting. Untuk itu perlu dibuat path url nya
    - Buka core/urls.py, tambahkan:
        `path('api-auth/', include('rest_framework.urls', namespace='rest_framework')) `
    - ketika mengakses blog_api, akan muncul button login di kanan atas
    
- 1.3 project level permission
    - project level permission = level project, misal: blog_api
    - pengaturan permission pada core/settings.py:
        - AllowAny --> semua bisa crud meskipun bukan user
        - IsAuthenticated --> harus terdaftar disalah satu user
        - IsAdminUser  --> harus superuser
        - IsAuthenticatedOrReadOnly --> user yang authenticated bisa update delete, user anonim hanya bisa read
    - 
    - .
- 1.4. User level permission
    - setiap add user baru (di admin panel), kita bisa mengatur grup dan permissionnya melalui gui
    - misal buat user adni, hanya diberi akses view saja pada blog

- 1.5. View level permission
    - view level permission = dipasang pada object yang mengandung queryset misal: views.py/PostList()
    
        - buka blog_api/view.py
        - from rest_framework.permissions import IsAdminUser
        - pada PostList tambahkan :
            - permission_classes = [IsAdminUser]
            - akses /api, Maka PostList() hanya bisa dilihat ketika user login sebagai admin
        - atau:
            - permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
            - akses /api, Maka permission akan mengikuti settingan pada user level permission

## 2. Custom Permissions
- 2.1. permissions (api)--> HTTP request(react)
    - permission di api harus bisa diakses CRUD dari react
    - Rule crud http:
        - view -> GET
        - delete -> DELETE
        - change -> PUT PATCH
        - add -> POST


