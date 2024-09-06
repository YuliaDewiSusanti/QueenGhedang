from django.shortcuts import render, redirect
from website.models import Custumer, Kategori, Kontak, Profil, Product, Slide
from django.contrib.auth.decorators import login_required
from website.decorators import pilihan_login, ijinkan_pengguna
from .forms import TransaksiStatusForm, ProfilForm, KategoriForm, ProductForm, SlideForm, CustumerForm, UserForm, InputTrackingForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from cart.models import Transaksi, DetailTransaksi
from django.db.models import Count, Q

@login_required(login_url='loginpage')
@pilihan_login
def beranda_admin(request):
    jmlKategori = Kategori.objects.filter(aktif=True).count()
    jmlCustumer = Custumer.objects.count()
    jmlSlide = Slide.objects.filter(aktif=True).count()
    jmlprodukminuman = Product.objects.filter(menu="MINUMAN").count()
    jmlprodukmakanan = Product.objects.filter(menu="MAKANAN").count()
    jmlprodukcamilan = Product.objects.filter(menu="CAMILAN").count()
    context = {
        'judul': 'Beranda',
        "jmlKategori":jmlKategori,
        "jmlCustumer":jmlCustumer,
        "jmlSlide":jmlSlide,
        "jmlprodukminuman":jmlprodukminuman,
        "jmlprodukmakanan":jmlprodukmakanan,
        "jmlprodukcamilan":jmlprodukcamilan,
        
    }
    return render(request, 'admin_beranda.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def profil_admin(request):
    profil = Profil.objects.get(id=1)
    form = ProfilForm(instance=profil)
    if request.method == 'POST':
        formedit = ProfilForm(request.POST,request.FILES, instance=profil)
        if formedit.is_valid():
            formedit.save()
            return redirect('profil_admin')
    context = {
        'judul': 'Profil',
        'form':form
    }
    return render(request, 'admin_profil.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def kategori_admin(request):
    kategori = Kategori.objects.all()
    context = {
        'data': kategori,
        'judul': 'Kategori',
    }
    return render(request, 'admin_kategori.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator'])    
def formkategori_admin(request):
    form = KategoriForm()
    if request.method == 'POST':
        formsimpan = KategoriForm(request.POST)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('kategori_admin')
    context = {
        'judul': 'Form Kategori',
        'form':form
    }
    return render(request, 'admin_formkategori.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def editkategori_admin(request, slug):
    kategori = Kategori.objects.get(slug=slug)
    form = KategoriForm(instance=kategori)
    if request.method == 'POST':
        formsimpan = KategoriForm(request.POST, instance=kategori)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('kategori_admin')
    context = {
        'judul': 'Form Edit Kategori',
        'form':form
    }
    return render(request, 'admin_formkategori.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def deletekategori_admin(request, pk):
    hapus = Kategori.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('kategori_admin')

    context = {
        'judul': 'Form Hapus Kategori',
        'hapus':hapus  
    }
    return render(request, 'admin_hapuskategori.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def product_admin(request):
    product = Product.objects.all()
    context = {
        'data': product,
        'judul': 'Product',
    }
    return render(request, 'admin_product.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator'])    
def formproduct_admin(request):
    form = ProductForm()
    if request.method == 'POST':
        formsimpan = ProductForm(request.POST,request.FILES)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('product_admin')
    context = {
        'judul': 'Form Product',
        'form':form
    }
    return render(request, 'admin_formproduct.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def editproduct_admin(request, slug):
    product = Product.objects.get(slug=slug)
    form = ProductForm(instance=product)
    if request.method == 'POST':
        formsimpan = ProductForm(request.POST,request.FILES, instance=product)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('product_admin')
    context = {
        'judul': 'Form Edit Product',
        'form':form
    }
    return render(request, 'admin_formproduct.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def deleteproduct_admin(request, pk):
    hapus = Product.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('product_admin')
    context = {
        'judul': 'Form Hapus Product',
        'hapus':hapus  
    }
    return render(request, 'admin_hapusproduct.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def slide_admin(request):
    slide = Slide.objects.all()
    context = {
        'data': slide,
        'judul': 'Slide',
    }
    return render(request, 'admin_slide.html', context)
@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def formslide_admin(request):
    form = SlideForm()
    if request.method == 'POST':
        formsimpan = SlideForm(request.POST,request.FILES)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('slide_admin')
    context = {
        'judul': 'Form Slide',
        'form':form
    }
    return render(request, 'admin_formslide.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def editslide_admin(request, pk):
    slide = Slide.objects.get(id=pk)
    form = SlideForm(instance=slide)
    if request.method == 'POST':
        formsimpan = SlideForm(request.POST,request.FILES, instance=slide)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('slide_admin')
    context = {
        'judul': 'Form Edit Slide',
        'form':form
    }
    return render(request, 'admin_formslide.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def deleteslide_admin(request, pk):
    hapus = Slide.objects.get(id=pk)
    if request.method == 'POST':
        hapus.delete()
        return redirect('slide_admin')
    context = {
        'judul': 'Form Hapus Slide',
        'hapus':hapus  
    }
    return render(request, 'admin_hapusslide.html', context)


@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def custumer_admin(request):
    custumer = Custumer.objects.all()
    context = {
        'data': custumer,
        'judul': 'Custumer',
    }
    return render(request, 'admin_custumer.html', context)


@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def deletecustumer_admin(request, pk):
    hapus = Custumer.objects.get(id=pk)
    id_user = User.objects.get(id=hapus.user.id)
    if request.method == 'POST':
        hapus.delete()
        id_user.delete()
        return redirect('custumer_admin')
    context = {
        'judul': 'Form Hapus Custumer',
        'hapus':hapus  
    }
    return render(request, 'admin_hapuscustumer.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def pemesananambildilokasi_admin(request):
    dilokasi = Transaksi.objects.filter(keterangan_pesanan="ditempat")
    context = {
        'data': dilokasi,
        'judul': 'Transaksi Pemesanan Ambil di Tempat',
    }
    return render(request, 'admin_pemesananambildilokasi.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def kontak_admin(request):
    kontak = Kontak.objects.all()
    context = {
        'data': kontak,
        'judul': 'Kontak',
    }
    return render(request, 'admin_kontak.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def detailpemesananambildilokasi_admin(request,transaksi):
    id_transaksi = Transaksi.objects.get(no_transaksi=transaksi)
    form =TransaksiStatusForm(instance=id_transaksi)
    detail = DetailTransaksi.objects.filter(no_transaksi=id_transaksi.no_transaksi).order_by('-id')
    if request.method == 'POST':
        formsimpan = TransaksiStatusForm(request.POST, instance=id_transaksi)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('pemesananambildilokasi_admin')
    context = {
        'data': detail,
        "id_transaksi":id_transaksi,
        "form":form,
        'judul': 'Detail Transaksi Pemesanan Ambil di Tempat',
    }
    return render(request, 'admin_detailpemesananambildilokasi.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def pemesanandiantar_admin(request):
    diantar = Transaksi.objects.filter(keterangan_pesanan="dilokasi")
    context = {
        'data': diantar,
        'judul': 'Transaksi Pemesanan di Antar ',
    }
    return render(request, 'admin_pemesanandiantar.html', context)


@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def detailpemesanandiantar_admin(request,transaksi):
    id_transaksi = Transaksi.objects.get(no_transaksi=transaksi)
    form =TransaksiStatusForm(instance=id_transaksi)
    detail = DetailTransaksi.objects.filter(no_transaksi=id_transaksi.no_transaksi).order_by('-id')
    if request.method == 'POST':
        formsimpan = TransaksiStatusForm(request.POST, instance=id_transaksi)
        if formsimpan.is_valid():
            formsimpan.save()
            return redirect('pemesanandiantar_admin')
    context = {
        'data': detail,
        "id_transaksi":id_transaksi,
        "form":form,
        'judul': 'Detail Transaksi Pemesanan di Antar Kerumah',
    }
    return render(request, 'admin_detailpemesanandiantar.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def trackingpemesanandiantar_admin(request):
    diantar = Transaksi.objects.annotate(total=Count('tracking__transaksi__id')).filter(keterangan_pesanan="dilokasi", status="Pengiriman")
    context = {
        'data': diantar,
        'judul': 'Tracking Transaksi Pemesanan di Antar ke rumah',
    }
    return render(request, 'admin_trackingpemesanandiantar.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['administrator']) 
def inputtrackingpemesanandiantar_admin(request,transaksi):
    id_transaksi = Transaksi.objects.get(no_transaksi=transaksi)
    form =InputTrackingForm()
    
    if request.method == 'POST':
        formsimpan = InputTrackingForm(request.POST)
        if formsimpan.is_valid():
            simpan = formsimpan.save()
            simpan.transaksi = id_transaksi
            simpan.save()
            return redirect('trackingpemesanandiantar_admin')
    context = {

        "id_transaksi":id_transaksi,
        "form":form,
        'judul': 'Input Tracking Transaksi Pemesanan di Antar ke rumah',
    }
    return render(request, 'admin_inputtrackingpemesanandiantar.html', context)