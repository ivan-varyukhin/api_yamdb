from django.core.mail import EmailMessage
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from reviews import models
from . import filters
from . import serializers
from . import mixins
from . import permissions


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UsersSerializer
    permission_classes = (IsAuthenticated, permissions.IsAdmin,)
    lookup_field = 'username'
    filter_backends = (SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = serializers.UsersSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = serializers.UsersSerializer(
                    request.user,
                    data=request.data,
                    partial=True,
                )
            else:
                serializer = serializers.NotAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True,
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)


class APIGetToken(APIView):
    def post(self, request):
        serializer = serializers.GetTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data
        try:
            user = User.objects.get(username=data['username'])
        except User.DoesNotExist:
            return Response(
                {'username': 'Такой пользователь не найден!'},
                status=status.HTTP_404_NOT_FOUND)
        if data.get('confirmation_code') == user.confirmation_code:
            token = RefreshToken.for_user(user).access_token
            return Response({'token': str(token)},
                            status=status.HTTP_201_CREATED)
        return Response(
            {'confirmation_code': 'Неверный код подтверждения!'},
            status=status.HTTP_400_BAD_REQUEST)


class APISignup(APIView):
    permission_classes = (AllowAny,)

    @staticmethod
    def send_email(data):
        email = EmailMessage(
            subject=data['email_subject'],
            body=data['email_body'],
            to=[data['to_email']]
        )
        email.send()

    def post(self, request):
        serializer = serializers.SignUpSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        email_body = (
            'Код подтвержения: {user.confirmation_code}'
        )
        data = {
            'email_body': email_body,
            'to_email': user.email,
            'email_subject': 'Код подтвержения для доступа к API'
        }
        self.send_email(data)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CategoryViewSet(mixins.CustomMixinSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (SearchFilter, )
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(mixins.CustomMixinSet):
    queryset = models.Genre.objects.all()
    serializer_class = serializers.GenreSerializer
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(ModelViewSet):
    queryset = models.Title.objects.all().annotate(
        rating=Avg('reviews__score')).order_by('id')
    http_method_names = ['get', 'post', 'patch', 'delete']
    permission_classes = (permissions.IsAdminOrReadOnly,)
    filter_backends = (DjangoFilterBackend, )
    filterset_class = filters.TitlesFilter

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return serializers.TitleSerializerRetviewe
        return serializers.TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.ReviewSerializer
    permission_classes = (permissions.IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        queryset = models.Review.objects.filter(title=title_id)
        return queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(models.Title, id=title_id)
        serializer.save(author=self.request.user, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (permissions.IsAuthorOrAdminOrReadOnly,)

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(models.Review, id=review_id)
        new_queryset = review.comments.filter(
            review=review_id,
            review__title=title_id)
        return new_queryset

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        author = self.request.user
        text = self.request.data.get('text')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            models.Review, id=review_id, title__id=title_id
        )
        serializer.save(author=author, review=review, text=text)
