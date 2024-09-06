from django import forms
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from website.models import Profil, Kategori, Product, Slide, Custumer
from cart.models import Transaksi, Tracking

class ProfilForm(ModelForm):
    class Meta:
        model = Profil
        fields= '__all__'
class KategoriForm(ModelForm):
    class Meta:
        model = Kategori
        fields=['nama','aktif']
    labels = {
            'nama': 'Nama Kategori:',
        } 

class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields=['kategori','nama_produk','gambar','gambar_satu','gambar_dua','gambar_tiga','gambar_empat','gambar_lima','keterangan','harga','no_whatsup','diskon','stock','keterangan_barang','menu']
    
        widgets = {

            'no_whatsup': forms.TextInput(attrs={'class': 'form-control','placeholder':'628xxxxxxxxxx'}),
            'stock': forms.NumberInput(attrs={'class': 'form-control'}),

        }
class SlideForm(ModelForm):
    class Meta:
        model = Slide
        fields=['judul','gambar_slide','aktif']

    
class CustumerForm(ModelForm):
    class Meta:
        model = Custumer
        fields=['nama','wa','alamat','email']
        widgets = {
            'wa': forms.TextInput(attrs={'class': 'form-control','placeholder':'628xxxxxxxxxx'}),

        }
class TransaksiStatusForm(ModelForm):
    class Meta:
        model = Transaksi
        fields=['status']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),

        }
        labels = {
            'status': 'Ubah Status:',
        } 

class UserForm(ModelForm):
    class Meta:
        model= User
        fields =['username']
        help_texts ={
            'username':''
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control','required':'required'}),
        }
        labels = {
            'username': 'Username*',
        }
    
class InputTrackingForm(ModelForm):
    class Meta:
        model = Tracking
        fields=['tanggal_tracking','jam_tracking','deskripsi']
        widgets = {
            'tanggal_tracking': forms.TextInput(attrs={'class': 'form-control','type':'date'}),

        }
        