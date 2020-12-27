from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView
from rest_framework.views import APIView
from blog.models import Post
from .serializers import PostSerializer


# Create your views here.
class PostList( ListCreateAPIView):
    queryset = Post.postobjects.all()
    serializer_class = PostSerializer


class PostDetail(RetrieveDestroyAPIView):
    pass
