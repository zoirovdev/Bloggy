from .models import Essay
from .serializers import EssaySerializer

from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from drf_spectacular.utils import extend_schema

class EssayList(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=
            { 
            'application/json': EssaySerializer, 
            'multipart/form-data': EssaySerializer  
            },
        responses=EssaySerializer
    )
    def post(self, request):
        serializer = EssaySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_201_CREATED)
    
    @extend_schema(responses=EssaySerializer)
    def get(self, request):
        essays = Essay.objects.all()
        serializer = EssaySerializer(essays, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class EssayDetail(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    @extend_schema(
        request=
        { 
            'application/json': EssaySerializer, 
            'multipart/form-data': EssaySerializer  
        },
        responses=EssaySerializer,
    )
    def put(self, request, pk):
        essay = Essay.objects.get(pk=pk)
        serializer = EssaySerializer(essay, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(responses=EssaySerializer)
    def get(self, reuqest, pk):
        essay = Essay.objects.get(pk=pk)
        serializer = EssaySerializer(essay)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
    @extend_schema(
        responses=EssaySerializer
    )
    def delete(self, request, pk):
        essay = Essay.objects.get(pk=pk)
        essay.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    
class UserEssayView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(responses=EssaySerializer)
    def get(self, request, pk):
        essays = Essay.objects.filter(author=pk)
        serializer = EssaySerializer(essays, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    



