from django.contrib import admin
from django.conf.urls import url
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from rest_framework import routers
from api.totalSum_api import ExpenseViewSet

router = routers.DefaultRouter()
# router.register(r'expense', ExpenseViewSet)
router.register(r'catagoryleaderboards', ExpenseViewSet,basename='CatagoryLeaderBoards')


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('accounts.urls')),
    path('', include('expense.urls')),
    path('', include('charts.urls')),
    url(r'^', include('api.urls')),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^api/', include(router.urls)),
    path('', include('Friends.urls')),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
