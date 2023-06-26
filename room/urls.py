from django.urls import path
from room.views import RoomListAPIView, RoomRetrieveAPIView, BookCreateAPIView, AvailabilityAPIView

urlpatterns = [
    path('rooms', RoomListAPIView.as_view(), name='rooms'),
    path('rooms/<int:pk>', RoomRetrieveAPIView.as_view(), name='room-retrieve'),
    path('rooms/<int:pk>/book/', BookCreateAPIView.as_view(), name='book-create'),
    path('rooms/<int:pk>/availability', AvailabilityAPIView.as_view(), name='availabilities'),
]
