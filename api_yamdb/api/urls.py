from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = 'api'

router = DefaultRouter()
router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    viewset=views.ReviewViewSet, basename='reviews'
)
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    viewset=views.CommentViewSet,
    basename='comments'
)
router.register(
    'users',
    views.UsersViewSet,
    basename='users'
)
router.register(
    'categories',
    views.CategoryViewSet,
    basename='categories',
)
router.register(
    'titles',
    views.TitleViewSet,
    basename='titles'
)
router.register(
    'genres',
    views.GenreViewSet,
    basename='genres'
)

urlpatterns = [
    path('v1/auth/token/', views.APIGetToken.as_view(), name='get_token'),
    path('v1/auth/signup/', views.APISignup.as_view(), name='signup'),
    path('v1/', include(router.urls)),
]
