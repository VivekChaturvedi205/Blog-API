from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import RegisterSerializer,LoginSerializer

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import RegisterSerializer

class Signup(APIView):
    def post(self, request):
        try:
            data = request.data
            profile_pic = request.FILES.get('profile_pic') 
            data['profile_pic'] = profile_pic
            
            serializer = RegisterSerializer(data=data)
            
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Please check your input'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            serializer.save()
            
            return Response({
                'data': {},
                'message': 'Registered Successfully'
            }, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'An error occurred, please check your input'
            }, status=status.HTTP_400_BAD_REQUEST)


class login(APIView):
    def post(self, request):
        try:
            data=request.data
            serializer=LoginSerializer(data=data)
            if not serializer.is_valid():
                return Response({
                    'data': serializer.errors,
                    'message': 'Please check your input'
                }, status=status.HTTP_400_BAD_REQUEST)
                
            response=serializer.get_jwt_token(serializer.data)                
            return Response(response,status=status.HTTP_200_OK)            
        except Exception as e:
            print(e)
            return Response({
                'data': {},
                'message': 'An error occurred, please check your input'
            }, status=status.HTTP_400_BAD_REQUEST)