from django.urls import path
from . import views


urlpatterns = [
    path('', views.beranda_admin, name='beranda_admin'),
    path('profil/', views.profil_admin, name='profil_admin'),

    path('kategori-admin/', views.kategori_admin, name='kategori_admin'),
    path('form-kategori/', views.formkategori_admin, name='formkategori_admin'),
    path('edit-kategori/<str:slug>', views.editkategori_admin, name='editkategori_admin'),
    path('delete-kategori/<str:pk>', views.deletekategori_admin, name='deletekategori_admin'),

    path('product-admin/', views.product_admin, name='product_admin'),
    path('form-product/', views.formproduct_admin, name='formproduct_admin'),
    path('edit-product/<str:slug>', views.editproduct_admin, name='editproduct_admin'),
    path('delete-product/<str:pk>', views.deleteproduct_admin, name='deleteproduct_admin'),

    path('slide-admin/', views.slide_admin, name='slide_admin'),
    path('form-slide/', views.formslide_admin, name='formslide_admin'),
    path('edit-slide/<str:pk>', views.editslide_admin, name='editslide_admin'),
    path('delete-slide/<str:pk>', views.deleteslide_admin, name='deleteslide_admin'),

    path('custumer/', views.custumer_admin, name='custumer_admin'),
    path('delete-custumer/<str:pk>', views.deletecustumer_admin, name='deletecustumer_admin'),
    
    path('kontak/', views.kontak_admin, name='kontak_admin'),

    path('pemesanan-ditempat/', views.pemesananambildilokasi_admin, name='pemesananambildilokasi_admin'),
    path('pemesanan-ditempat/<str:transaksi>', views.detailpemesananambildilokasi_admin, name='detailpemesananambildilokasi_admin'),

    path('pemesanan-diantar/', views.pemesanandiantar_admin, name='pemesanandiantar_admin'),
    path('pemesanan-diantar/<str:transaksi>', views.detailpemesanandiantar_admin, name='detailpemesanandiantar_admin'),

    path('tracking-pemesanan-diantar/', views.trackingpemesanandiantar_admin, name='trackingpemesanandiantar_admin'),

    path('tracking-pemesanan-diantar/<str:transaksi>', views.inputtrackingpemesanandiantar_admin, name='inputtrackingpemesanandiantar_admin'),
]