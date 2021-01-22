from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from blog.models import Post, Category
from django.contrib.auth.models import User
from rest_framework.test import APIClient


# Create your tests here.
class PostTest(APITestCase):
    # Simulasi Read/view
    def test_view_post(self):
        url = reverse('blog_api:listcreate')# blog_api = nama api, listcreate = nama root path --> urls.py
        response = self.client.get(url, format='json') # client adalah simulasi dari browser, GET method untuk read
        self.assertEqual(response.status_code, status.HTTP_200_OK) #koneksi dengan http berhasil, url harus http:200 untuk test berhasil

    # Simulasi Post
    def create_post(self):
        self.test_category = Category.objects.create(name='django') # Buat category
        self.test_user1 = User.objects.create_superuser(username='test_user1', password='123456789') # buat user sbg superuser/admin

        self.client.login(username=self.test_user1.username, password='123456789') # Simulasi login menggunakan admin

        data = {"title":"new", "author":1, "excerpt":"new", "content":"new"} # Simulasi input data
        url = reverse('blog_api:listcreate')
        response = self.client.post(url, data, format='json') # POST method untuk write/input data
        self.assertEqual(response.status_code, status.HTTP_200_OK) #koneksi dengan http berhasil

        # root = reverse(('blog_api:detailcreate'), kwargs={'pk':1})
        # response = self.client.get(url, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

    # SImulasi Update
    def test_post_update(self):

        client = APIClient()

        self.test_category = Category.objects.create(name='django') # Simulasi buat kategori
        self.test_user1 = User.objects.create_user(username='test_user1', password='123456789') #Simulasi membuat user1
        self.test_user2 = User.objects.create_user(username='test_user2', password='123456789') #Simulasi membuat user2
        #
        test_post = Post.objects.create(
            category_id=1,
            title='Post Title',
            excerpt='Post Excerpt',
            content='Post Content',
            slug='post-title',
            author_id=1,
            status='published')
        #simulasi user login
        client.login(username=self.test_user1.username, password='123456789')

        url = reverse(('blog_api:detailcreate'), kwargs={'pk':1})
        
        #Simulasi user edit post/PUT
        # id=1 --> author=1
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