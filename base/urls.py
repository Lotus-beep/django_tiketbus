from django.urls import path
from .views import *

urlpatterns = [
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', CustemRefresTokenView.as_view(), name='token_refresh'),
    path('notes/', get_notes),
    path('logout/', logout),
    path('Register/', Register),
    path('auth/', is_authenticated),
    path('addBangku/', CreateTypeTiket),
    path('addPesanan/', CreatePesanan),
    path('getdata/', gettiket),
    path('getdata/<int:id>/', gettiketid),
    path('createTiket/',get_tiket)
]