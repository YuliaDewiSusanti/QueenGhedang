from django.urls import path
from .import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', views.beranda, name='beranda'),
    path('profil/', views.profil, name='profil'),
    path('<slug:slug>', views.kategori, name='kategori'),
    path('<slug:kategori_slug>/<slug:slug>', views.product, name='product'),
    path('kontak/', views.KontakView.as_view(), name='kontak'),
    path('checkout/', login_required(login_url='loginpage')(views.CheckoutView.as_view()), name='checkout'),
    path('register/', views.register, name='register'),
    path('login/', views.loginpage, name='loginpage'),
    path('logout/', views.logoutpage, name='logoutpage'),
    path('histori/', views.histori, name='histori'),
    path('tracking/', views.tracking, name='tracking'),
    path('tracking-booking-antar/<str:transaksi>/', views.trackingantar, name='trackingantar'),
    path('cari/', views.cari, name='cari'),


    path('isi-vitual-account/<str:notransaksi>/', views.isivitual, name='isivitual'),
    path('midtrans_callback/', views.midtrans_callback, name='midtrans_callback'),

]