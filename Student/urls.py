from django.urls import path
from .views import *

urlpatterns = [
    path('userIndex/',userIndex, name='userIndex'),
    path('ReserveItem/<int:itemId>',reserveItem, name='reserveItem'),
    path('ReleaseItem/<int:itemId>',ReleaseItem, name='releaseItem'),
    path('ChangePassword/',ChangePassword, name='changePassword'),
    path('UpdateProfile/',UpdateUser, name='updateUser'),
    path('Reservations/',CheckReservation, name='checkRes'),
    path('userLogouot/',userLogout, name='userLogout'),
    # path('searchBy/',searchItem, name='searchItem'),

]