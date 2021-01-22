from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, RetrieveDestroyAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import SAFE_METHODS, BasePermission, IsAdminUser, DjangoModelPermissionsOrAnonReadOnly, DjangoModelPermissions, IsAuthenticatedOrReadOnly


# Create your views here.

#CUSTOM PERMISSION
class PostUserWritePermission(BasePermission):
    message = 'Editing posts is restricted to the author only.'

    # Method custom permission
    # Menggunakan has_object_permission karena kita menggunakan object permission
    def has_object_permission(self, request, view, obj):
        
        if request.method in SAFE_METHODS:
            return True
        # menjadikan author sbg objek = user login
        # kenapa author? karena pada form, dia menggunakan username sebagai valuenya
        # username aris -> membuka postingan dengan author aris
        return obj.author == request.user
      
# Menampilkan view  ( misal: http://127.0.0.1:8000/api)
# ListCreateAPIView --> menampilkan view dengan metode GET dan POST (Read post dan Form input post)
class PostList(ListCreateAPIView):
    permission_classes = [IsAuthenticatedOrReadOnly]
    # permission_classes = [DjangoModelPermissions] # Halaman ini menggunakan settingan user di admin panel, lebih fleksibel
    # permission_classes = [IsAdminUser]
    # permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer

# Menampilkan Post detail ( misal: http://127.0.0.1:8000/api/1)
# RetrieveUpdateDestroyAPIView --> menampilkan form view dengan metode GET, PUT, dan DELETE (Read, update, delete)
class PostDetail(RetrieveUpdateDestroyAPIView, PostUserWritePermission):
    permission_classes = [PostUserWritePermission] # Halaman ini menggunakan custom permission, sehingga user hanya bisa PUT dan DELETE post detail miliknya sendiri
    queryset = Post.objects.all()
    serializer_class = PostSerializer


# Documentation 
# DRF Generics view: membuat view dengan berbagai behaviour-> https://www.django-rest-framework.org/api-guide/generic-views/
# DRF Permissions : membuat permission  -> https://www.django-rest-framework.org/api-guide/permissions