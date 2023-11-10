from django.urls import path
from . import views
from rest_framework import routers
from django.conf import settings
from django.conf.urls import include
from django.conf.urls.static import static

router = routers.DefaultRouter()
router.register('register', views.DataViewSet)

urlpatterns = [
    path('', views.view),
    path('<int:user_id>/', views.detail),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
