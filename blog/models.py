from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

# Model Category
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

#Model Post
class Post(models.Model):

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter(status='published')

    options = (('draft', 'Draft'),('published', 'Published'),)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, default=1) #Foreign key, mengambil data dari class category diatas
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    content = models.TextField()
    slug = models.SlugField(max_length=250, unique_for_date='published')
    published = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts') #Foreign key, mengambil dari nama User login
    status = models.CharField(max_length=10, choices=options, default='published')
    
    # method dari luar bisa mengakses semua object model melalui var dibawah ini:
    objects = models.Manager() #default manager, anggotanya semua class dg param model.manager, misal memasukkan data 'categori' dan 'title' dari luar, bisa menggunakan -->Post.objects.create(category_id=1, title='Post Title')
    postobjects = PostObjects() #custom manager, misal akses: Post.postobjects.get(id=1) alih2 Post.PostObjects.get(id=1)-->hasilnya tidak bisa diakses dari luar, untuk itu di namai ulang

    class Meta:
        ordering = ('-published', )

    def __str__(self):
        return self.title