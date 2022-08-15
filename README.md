Deploy docker

# DAFTAR ISI
- [ A. BASIC_BACKEND-API ](#A)
    - [ 1. Instalasi ](#A1)
        - [ 1.1. Instalasi Django ](#A11)
        - [ 1.2. Membuat superuser ](#A12)
        - [ 1.3 Menambahkan installed apps ](#A13)
        - [ 1.4. Menjalankan server django ](#A14)
    - [ 2. Redirect URL ](#A2)
        - [ 2.1. Redirect url bawaan django ke url buatan sendiri ](#A21)
        - [ 2.2. Membuat urls.py untuk  __blog__ dan __blog_api__ ](#A22)

    - [ 3. Template ](#A3)
    - [ 4. Models ](#A4)
        - [ 4.1. Blog/Models.py ](#A41)
    - [ 5. Blog_api ](#A5)
        - [ 5.1. Blog_api/serializers.py ](#A51)
        - [ 5.2. Blog_api/views.py ](#A52)
        - [ 5.3. Blog_api/urls.py ](#A53)
    - [ 6. model (blog) -> serializers (api) -> Views (api) -> urls (api) ](#A6)
        - [ 6.1. Pengetesan PostList() -> GET dan POST ](#A61)
        - [ 6.2. Menampilkan menu Blog: Posts dan categorys di admin ](#A62)
        - [ 6.3. Tes PostDetail() -> DELETE ](#A63)
    - [ 7. Unit Testing blog dan blog_api ](#A7)
        - [ 7.1. persiapan testing, Setting permission untuk rest ](#A71)
        - [ 7.2. coverage ](#A72)
        - [ 7.3. Testing blog ](#A73)
        - [ 7.4. Testing blog_api ](#A74)
    

- [ B. FRONT END (REACT) ](https://github.com/ArisDjango/CrudVeryAcademyReact2)

- [ C. PERMISSION DAN CUSTOM PERMISSION ](#C)
    - [ 1. Default Permission ](#C1)
        - [ 1.1. Pendahuluan ](#C11)
        - [ 1.2. Authentification Url ](#C12)
        - [ 1.3. project level permission ](#C13)
        - [ 1.4. User level permission ](#C14)
        - [ 1.5. View level permission ](#C15)
        - [ 1.6. Studi kasus ](#C16)
    - [ 2. Custom Permission ](#C2)
        - [ 2.1. permissions (api)--> HTTP request(react) ](#C21)
    

<a name="A"></a>
# A. BASIC_BACKEND-API
<a name="A1"></a>
## 1. Instalasi
<a name="A11"></a>
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

<a name="A12"></a>
- 1.2. Membuat superuser
    - `python manage.py createsuperuser`
    - isi username, email, isi password aris1985

<a name="A13"></a>
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

<a name="A14"></a>
- 1.4. Menjalankan server django
    - `python manage.py runserver`
    - jika berhasil, akan muncul halaman django

<a name="A2"></a>
## 2. Redirect URL
<a name="A21"></a>
- 2.1. Redirect url bawaan django ke url buatan sendiri
    - Fungsi: melakukan redirect url bawaan django ke urls.py buatan sendiri

    - buka file core>urls.py, code:
        ```py
        from django.contrib import admin
        from django.urls import path
        from django.conf.urls import include

        urlpatterns = [
            path('admin/', admin.site.urls),
            path('', include('blog.urls',)),
            path('api/',include('blog_api.urls'))
        ]
        ```
<a name="A22"></a>
- 2.2. Membuat urls.py untuk  __blog__ dan __blog_api__
    - Buat blog/urls.py
        - code:
        ```py
        from django.urls import path
        from django.views.generic import TemplateView

        app_name = 'blog'

        urlpatterns = [
            path('', TemplateView.as_view(template_name="blog/index.html")),

        ]
        ```
    - Buat blog_api/urls.py
        - code:
        ```py
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
<a name="A3"></a>        
## 3. Template
- Menggunakan Template
    - Membuat dir baru `templates/blog/index.html`
    - dipengaruhi path yang ada di blog.urls
    - isi index.html dengan content sederhana
    - registrasi di settings.py
        - di templates>dirs
            ```py
            'DIRS': [BASE_DIR / 'templates'],
            ```
    - Jalankan `python manage.py runserver`
    - Jika berhasil, maka localhost akan menampilkan content dari index.html

<a name="A4"></a>
## 4. Models
<a name="A41"></a>
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
        ```py
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

<a name="A5"></a>
## 5. Blog_api
<a name="A51"></a>
- 5.1. Blog_api/serializers.py
    - Fungsi: Mengambil data dari model
    - ======================
    - code:
        ```py
        from rest_framework import serializers
        from blog.models import Post

        class PostSerializer(serializers.ModelSerializer):
            class Meta:
                model = Post
                fields = ('id', 'title', 'author', 'excerpt', 'content', 'status')
       ```
<a name="A52"></a>
- 5.2. Blog_api/views.py
    - Fungsi:
        - Mengambil data dan menampilkan serializer dalam bentuk form sederhana
        - ListCreateAPIView = menampilkan view api berupa fungsi GET dan POST
        - RetrieveDestroyAPIView = fungsi DELETE dari api (sementara pass, akan dibahas nanti)
    - ===========================
    - code:
        ```py
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
<a name="A53"></a>
- 5.3. Blog_api/urls.py
    - Fungsi: by pass Blog_api/views.py (PostDetail/PostList)  ke urls.py, sehingga bisa diakses melalui http://127.0.0.1:8000/api/
    - Argumen post detail `<int:pk>` = mengambil id(int) dengan primary key yang sedang aktif. Misal: http://127.0.0.1:8000/api/1
    - ================================
    - code:
        ```py
        from django.urls import path
        from .views import PostList, PostDetail

        app_name = 'blog_api'

        urlpatterns = [
            path('<int:pk>/', PostDetail.as_view(), name='detailcreate'),
            path('', PostList.as_view(), name='listcreate')

        ]
        
        ```

<a name="A6"></a>
## 6. model (blog) -> serializers (api) -> Views (api) -> urls (api)
<a name="A61"></a>
- 6.1. Pengetesan PostList() -> GET dan POST
    - Fungsi: 
        - Mengetes koneksi data dari model diekstrak di serializer, di tampilkan di view, menggunakan alamat by pass dari urls
        - View http://127.0.0.1:8000/api/ akan Menghasilkan tampilan Post list dummy dengan fungsi GET dan POST hasil dari PostList()
    - ========================
       
    - buka http://127.0.0.1:8000/api/
    - Jika berhasil akan menampilkan form Post List dengan tombol GET dibagian atas untuk menampilkan output dan POST dibagian bawah form untuk input form.
    - form field 'author' mempunyai value winandiaris(superuser)
    - Coba isi seluruh form, lalu POST, maka akan menghasilkan error foreign keyconstraint failed
    - permasalahannya adalah ada 2 foreign key di blog/models, yaitu fields 'category' dan 'author'. 'category' default=1, namun format default ini belum dibuat, solusi ada di bab selanjutnya

<a name="A62"></a>
- 6.2. Menampilkan menu Blog: Posts dan categorys di admin
    - Fungsi:
        - register/menampilkan menu Posts dan categorys di admin panel. Hasil kompilasi input form bisa dilihat disini
        - contoh category bisa di input melalui admin panel, dengan begitu error double foreign key teratasi karena category sudah mempunyai defaults=1

    - ========================
    - Buka blog/admin.py
    - code:
        ```py
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

<a name="A63"></a>
- 6.3. Tes PostDetail() -> DELETE:
    - Fungsi: View http://127.0.0.1:8000/api/1 Menghasilkan tampilan Post detail dengan fungsi DELETE Post/category hasil dari PostDetail()
    - =========================
    - Masuk blog_api/views.py/PostDetail()
    - code:
        ```py
        class PostDetail(RetrieveDestroyAPIView):
            queryset = Post.objects.all()
            serializer_class = PostSerializer
        ```
    - Jika kita akses http://127.0.0.1:8000/api/1 maka akan muncul detail post
    - Jika kita DELETE, maka post akan hilang

<a name="A7"></a>
## 7. Unit Testing blog dan blog_api
<a name="A71"></a>
- 7.1. persiapan testing, Setting permission untuk rest
    - core/settings.py:
    - setting untuk memberikan permission ke semua endpoint
    - code:
        ```py
        REST_FRAMEWORK = {
        'DEFAULT_PERMISSION_CLASSES': [
            'rest_framework.permissions.AllowAny',
            ]
        }
        ```
<a name="A72"></a>
- 7.2. coverage
    - Fungsi: modul tampilan testing, sehingga mudah di inspeksi
    - Instalasi:
        - `pip install coverage`
        - `coverage run --omit='*venv*' manage.py test`
        - `coverage html`
        - maka akan otomatis membuat htmlcov
        - buka htmlcov/index.html, untuk melihat hasil test dalam bentuk html
        - maka akan muncul halaman test, terlihat mana yang masih missing, yaitu models.py ada 2 missing

<a name="A73"></a>
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
            ```py
            from django.test import TestCase
            from django.contrib.auth.models import User
            from blog.models import Post, Category
            ```
        - Membuat class test dan membuat method dummy data
            ```py
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
            ```py
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
            ```py
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
        ```py
            "python.linting.pylintArgs": [
                "--load-plugins",
                "pylint_django",
                "--errors-only",
                "--load-plugins pylint_django"
            ],
        ```

<a name="A74"></a>
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
        ```py
        from django.urls import reverse
        from rest_framework import status
        from rest_framework.test import APITestCase
        from blog.models import Post, Category
        from django.contrib.auth.models import User
        ```
        - Membuat class baru untuk test api:
            - Membuat method `test view post`

                ```py
                class PostTest(APITestCase):

                def test_view_post(self):
                    url = reverse('blog_api:listcreate')
                    response = self.client.get(url, format='json') 
                    self.assertEqual(response.status_code, status.HTTP_200_OK)
                ```
            - Membuat method test `create post test`:
                - var dummy data (category dan user):
                ```py
                def create_post(self):
                    self.test_category = Category.objects.create(name='django')
                    self.test_user1 = User.objects.create_user(username='test_user1', password='123456789')
                ```
                - var dummy post,url reverse, & response:
                ```py
                    data = {"title":"new", "author":1, "excerpt":"new", "content":"new"}
                    url = reverse('blog_api:listcreate')
                    response = self.client.post(url, data, format='json')

                ```
                - Test status response http 201: past post/get
                ```py
                    self.assertEqual(response.status_code, status.HTTP_201_OK) # koneksi setelah PUT/GET berhasil
                ```

<a name="B"></a>
# B. FRONT END (REACT)
Front end ada pada file terpisah [disini](https://github.com/ArisDjango/CrudVeryAcademyReact2)

<a name="C"></a>
# C. PERMISSION DAN CUSTOM PERMISSION
- [DRF Authentication Documentation](https://www.django-rest-framework.org/api-guide/authentication/)
- [DRF Permission Documentation](https://www.django-rest-framework.org/api-guide/permissions/)
<a name="C1"></a>
## 1. Default Permission
<a name="C11"></a>
- 1.1. Pendahuluan
    - Sejauh ini yang kita bangun:
        - Django RestAPI
        - React App yang mengkonsumsi RestAPI
    - Pada bab ini akan membahas sistem permission ketika user mengkases blog_api

    - .
<a name="C12"></a>
- 1.2. Authentification Url / Login button
    - Tujuan: Pada saat mengakses blog_api, perlu halaman login untuk mengotentifikasi user agar ketika masuk mempunyai hak sesuai permission setting. Untuk itu perlu dibuat path url nya
    - Buka core/urls.py, tambahkan:
        `path('api-auth/', include('rest_framework.urls', namespace='rest_framework')) `
    - ketika mengakses blog_api, akan muncul button login di kanan atas

<a name="C13"></a>
- 1.3 project level permission
    - Tujuan : mengatur permission pada level project, misal: blog_api, nantinya hanya admin yang bisa mengakses, anonim tidak bisa
    - buka core/settings.py:
        - pada bagian REST_FRAMEWORK = {
              'DEFAULT_PERMISSION_CLASSES':[
                  'rest_framework.permissions.IsAuthenticatedOrReadOnly'
              ]
        - Penjelasan macam2 permission:
            - IsAuthenticatedOrReadOnly --> user yang authenticated bisa CRUD (POST), user anonim hanya bisa read (GET)
            - AllowAny --> semua bisa crud meskipun bukan user
            - IsAuthenticated --> harus terdaftar disalah satu user
            - IsAdminUser  --> harus superuser

    - 
    - .

<a name="C14"></a>
- 1.4. User level permission
    - Tujuan: Mengatur permission untuk user
    - setiap add user baru (di admin panel), kita bisa mengatur grup dan permissionnya melalui gui
    - misal buat user adni, hanya diberi akses view saja pada blog
    - artinya user disini bisa juga diset sebagai superuser/admin

<a name="C15"></a>
- 1.5. Object level permission
    - Tujan: Mengatur permission pada level object, misal object view() pada page home, object post() pada page api, dll
    - view level permission = dipasang pada object yang mengandung queryset misal: views.py/PostList()
    
        - buka blog_api/view.py
        - from rest_framework.permissions import IsAdminUser
        - pada PostList tambahkan :
            - permission_classes = [IsAdminUser]
            - akses /api, Maka PostList() hanya bisa dilihat ketika user login sebagai admin
        - atau:
            - permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
            - akses /api, Maka permission akan mengikuti settingan pada user level permission

<a name="C16"></a>
- 1.6. Studi kasus
    - Studi kasus 1
        - pengaturan app blog_api:
            - project level -> admin
            - object level (view()) -> admin
            - user -> authUser CRUD
        - Maka user tidak bisa mengakses blog_api sama sekali (meskipun user punya akses CRUD), hanya admin yang bisa

    - Studi kasus 2
        - pengaturan app blog_api:
            - project level -> - IsAuthenticatedOrReadOnly
            - object level (view()) -> admin
            - user -> authUser CRUD
        - Maka user bisa mengakses blog_api, namun hanya GET/READ. Meskipun view level: admin

    - Studi kasus 3
        - pengaturan app blog_api:
            - project level -> admin
            - object level (view()) -> DjangoModelPermissionsOrAnonReadOnly
            - object level (delete()) -> admin
            - user -> authUser CRUD
        - Maka user bisa mengakses blog_api dan CRUD , meskipun project level: admin. Karena pada object level (view()) meng override/mengembalikan ke permission default user yaitu CRUD. namun hanya terbatas page view(), delete() hanya bisa diakses admin

<a name="C2"></a>
## 2. Custom Permissions
[dokumentasi](https://www.django-rest-framework.org/api-guide/permissions/#custom-permissions)
<a name="C21"></a>
- 2.1. Pendahuluan
    - Tujuan : Memberikan custom permission kepada user dengan skenario:
        - Asumsi, User punya POST content blog (yang memasukkan admin, karena untuk sementara user tidak bisa POST secara langsung dari api)
        - User bisa akses blog_api, bisa GET seluruh post, namun tidak bisa POST
        - User bisa akses halaman detail setiap POST (http://127.0.0.1:8000/api/1) namun hanya GET, tidak bisa DELETE
        - Hanya ketika User mengakses halaman detail post miliknya sendiri, mampu melakukan DELETE dan PUT

    - permissions (api)--> HTTP request(react)
    - permission di api harus bisa diakses CRUD dari react
    - Rule crud http di browser secara umum:
        - view/read -> GET
        - delete -> DELETE
        - change -> PUT PATCH
        - add -> POST

- 2.2. Implementasi
    - code:
    ```py
    from rest_framework.permissions import SAFE_METHODS, BasePermission
    ```
    - Method custom permission
    ```py
    class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    
    def has_object_permission(self, request, view, obj):
        
        if request.method in SAFE_METHODS:
            return True
        
        return obj.author == request.user
    ```
    - PostList()code:
    ```py
    class PostList(ListCreateAPIView):
    permission_classes = [DjangoModelPermissions]
    ```
    - PostDetail() code:
    ```py
    class PostDetail(RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission]
    ```

- 2.3. Unit Test
    - fgdf
    ```py
    def test_post_update(self):

        client = APIClient()

        self.test_category = Category.objects.create(name='django')
        self.test_user1 = User.objects.create_user(username='test_user1', password='123456789')
        self.test_user2 = User.objects.create_user(username='test_user2', password='123456789')
        
        test_post = Post.objects.create(
            category_id=1,
            title='Post Title',
            excerpt='Post Excerpt',
            content='Post Content',
            slug='post-title',
            author_id=1,
            status='published')
        
        client.login(username=self.test_user1.username, password='123456789')

        url = reverse(('blog_api:detailcreate'), kwargs={'pk':1})
        
        response = client.put( url, {
                'id':1,
                'title': 'new',
                'author': 1,
                'excerpt': 'new',
                'content': 'new',
                'status': 'published',
            }, format='json')
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    ```


