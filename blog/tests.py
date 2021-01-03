from django.test import TestCase
from django.contrib.auth.models import User
from blog.models import Post, Category

# Create your tests here.
class Test_Create_post(TestCase):

    # Method object dummy, param cls digunakan karena data di class ini hanya sementara, tidak terhubung ke instance utama
    @classmethod
    def setUpTestData(cls): 
        test_category = Category.objects.create(name='django') #dummy category='django'
        testuser1 = User.objects.create_user(username='test_user1', password='123456789') #dummy login username
        test_post = Post.objects.create(category_id=1, title='Post Title', excerpt='Post Excerpt', content='Post Content', slug='post-title', author_id=1, status='published') #dummy posting
        
    # Method Logic mengikuti model sebenarnya
    def test_blog_content(self): 
        post = Post.postobjects.get(id=1) # mengakses class Post di model, list query utama
        cat = Category.objects.get(id=1) # Mengakses class Category di model
        author = f'{post.author}' # Mengakses data di model
        excerpt = f'{Post.excerpt}'
        title = f'{post.title}'
        content = f'{post.content}'
        status = f'{post.status}'
    
        # Testing memberikan value variable dengan nilai yang benar
        # Misal, assertEqual->title = 'Post Title' sesuai dengan data di 'setUpTestData.title'
        self.assertEqual(author, 'test_user1')
        self.assertEqual(title, 'Post Title')
        self.assertEqual(content, 'Post Content')
        self.assertEqual(status, 'published')
        self.assertEqual(str(post), "Post Title")
        self.assertEqual(str(cat), "django")
        