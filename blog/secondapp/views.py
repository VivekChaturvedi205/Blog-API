from django.db.models import Q
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from .models import Blog
from .serializers import BlogSerializer
from django.core.paginator import Paginator
from django.http import Http404

class BlogView(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get(self, request):
        try:
            blogs = Blog.objects.filter(user=request.user)
            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))
            serializer = BlogSerializer(blogs, many=True)
            return Response({
                'data': serializer.data,
                'message': 'Blogs fetched successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'error': 'Internal Server Error',
                'details': str(e),
                'message': 'An error occurred, please check your input'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            data = request.data
            data['user'] = request.user.id
            serializer = BlogSerializer(data=data)

            if not serializer.is_valid():
                return Response({
                    'error': 'Validation Error',
                    'details': serializer.errors,
                    'message': 'Please check your input'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'Blog created successfully'
            }, status=status.HTTP_201_CREATED)

        except Exception as e:
            print(e)
            return Response({
                'error': 'Internal Server Error',
                'details': str(e),
                'message': 'An error occurred, please check your input'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def patch(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uuid=data.get('uuid')).first()

            if not blog:
                return Response({
                    'data': {},
                    'message': 'Invalid blog'
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog.user:
                return Response({
                    'data': {},
                    'message': 'You are not authorized to update this blog'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer = BlogSerializer(instance=blog, data=data, partial=True)

            if not serializer.is_valid():
                return Response({
                    'error': serializer.errors,
                    'message': 'Please check your input'
                }, status=status.HTTP_400_BAD_REQUEST)

            serializer.save()

            return Response({
                'data': serializer.data,
                'message': 'Blog updated successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'error': 'Internal Server Error',
                'details': str(e),
                'message': 'An error occurred, please check your input'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            data = request.data
            blog = Blog.objects.filter(uuid=data.get('uuid')).first()

            if not blog:
                return Response({
                    'data': {},
                    'message': 'Invalid blog uuid'
                }, status=status.HTTP_400_BAD_REQUEST)

            if request.user != blog.user:
                return Response({
                    'data': {},
                    'message': 'You are not authorized to delete this blog'
                }, status=status.HTTP_400_BAD_REQUEST)

            blog.delete()

            return Response({
                'message': 'Blog deleted successfully',
                'data': {}  
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'error': 'Internal Server Error',
                'details': str(e),
                'message': 'An error occurred, please check your input'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            

class PublicView(APIView):
    def get(self, request):
        try:
            blogs = Blog.objects.all().order_by('?')

            if request.GET.get('search'):
                search = request.GET.get('search')
                blogs = blogs.filter(Q(title__icontains=search) | Q(blog_text__icontains=search))

            page_number = request.GET.get('page', 1)

            try:
                page_number = int(page_number)
                if page_number < 1:
                    raise ValueError("Page number must be a positive integer.")
            except ValueError:
                raise Http404("Invalid page number.")

            paginator = Paginator(blogs, 1)
            blogs_page = paginator.page(page_number)

            serializer = BlogSerializer(blogs_page, many=True)
            return Response({
                'data': serializer.data,
                'message': 'Blogs fetched successfully'
            }, status=status.HTTP_200_OK)

        except Exception as e:
            print(e)
            return Response({
                'error': 'Internal Server Error',
                'details': str(e),
                'message': 'An error occurred, please check your input'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
