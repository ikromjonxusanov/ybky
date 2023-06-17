from django.urls import path
from room.views import RoomListAPIView, RoomRetrieveAPIView

urlpatterns = [
    path('rooms', RoomListAPIView.as_view(), name='rooms'),
    path('rooms/<int:pk>', RoomRetrieveAPIView.as_view(), name='room-retrieve')
]
