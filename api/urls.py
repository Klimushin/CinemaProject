from django.urls import include, path
from rest_framework import routers
from api.viewsets import UserRegisterAPIView, HallViewSet, SessionViewSet, TicketViewSet


app_name = 'api'
router = routers.DefaultRouter()
router.register(r'halls', HallViewSet)
router.register(r'sessions', SessionViewSet)
router.register(r'tickets', TicketViewSet)

urlpatterns = [
    path('api/register/', UserRegisterAPIView.as_view(), name='api_register'),
    path('api/', include(router.urls)),
]
