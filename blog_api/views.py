from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from blog.models import Post
from .serializers import PostSerializer
from rest_framework.permissions import IsAdminUser, DjangoModelPermissionsOrAnonReadOnly


# Create your views here.
class PostList( ListCreateAPIView):
    # permission_classes = [IsAdminUser]
    permission_classes = [DjangoModelPermissionsOrAnonReadOnly]
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer


class PostDetail(RetrieveDestroyAPIView):
    # pass
    queryset = Post.objects.all()
    serializer_class = PostSerializer
