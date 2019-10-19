from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from api.totalSum_api import ExpenseViewSet

router = routers.DefaultRouter()
router.register('userexpense', ExpenseViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('expense.urls')),
    path('', include('api.urls')),
    path('api/', include(router.urls)),
    path('', include('Friends.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
