from django.core.management import call_command
from django.http import HttpResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import CustomUser
from .serializers import UserSerializer,ContentSerializer
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .models import Content_item,Category
from django.http import Http404
from .permissions import IsAuthor,IsAdminUser
from.custom_seed import Command
from django.core.mail import send_mail
@api_view["POST"]
def create_admin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')

        # Call the management command and pass user data as arguments
        Command('custom_seed',request.data)

        return HttpResponse('Database seeded successfully!')
    else:
        return HttpResponse('Invalid request method')



class UserRegistration(APIView):
    permission_classes = (IsAuthenticated,)

    def send_email(self,subject,message,from_email,to_email):
        send_mail(subject,message,from_email,to_email)
        return None
    def post(self, request):
        if request.user.role == 'Author':
            serializer = UserSerializer(data=request.data)
            if serializer.is_valid():
                user = serializer.save()
                user.set_password(request.data['password'])
                user.save()
                subject = "Registration"
                message = "You Are Registered Successfully"
                recipient = request.data.email
                self.send_email(subject, message, 'from@example.com', [recipient])
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'message': 'You are not authorized to perform this action'},
                            status=status.HTTP_403_FORBIDDEN)


class UserLogin(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.user.role == 'Author':
            username = request.data.get('username')
            password = request.data.get('password')

            user = authenticate(username=username, password=password)
            if user:
                token, created = Token.objects.get_or_create(user=user)
                return Response({'token': token.key}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'message': 'You are not authorized to perform this action'},
                            status=status.HTTP_403_FORBIDDEN)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAdminUser])
def Admin_content_detail(request):
    if request.user.role=="Admin":
        try:
            content = Content_item.objects.all()
        except Content_item.DoesNotExist:
            raise Http404

        if request.method == 'GET':
            serializer = ContentSerializer(content)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = ContentSerializer(content, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        elif request.method == 'DELETE':
            content.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticated, IsAuthor])
def article_detail(request, pk):
    try:
        article = Content_item.objects.filter(auther=request.user.email)
    except Content_item.DoesNotExist:
        return Response(status=404)

    if request.method == 'GET':
        serializer = Content_item(article)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = Content_item(article, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)
    elif request.method == 'DELETE':
        article.delete()
        return Response(status=204)




@api_view(['GET'])
def content_search(request):
    query_params = request.query_params.get("ancd")
    if query_params:
        articles = Content_item.objects.filter(
            Content_item(title__icontains=query_params) |
            Content_item(body__icontains=query_params) |
            Content_item(summary__icontains=query_params) |
            Content_item(categories__name__icontains=query_params)
        )
        serializer = ContentSerializer(articles, many=True)
        return Response(serializer.data)
    else:
        return Response({"message": "No search query provided"}, status=400)