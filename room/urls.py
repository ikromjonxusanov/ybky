from django.urls import path
from room.views import RoomListAPIView

urlpatterns = [
    path('rooms', RoomListAPIView.as_view(), name='rooms')
]
