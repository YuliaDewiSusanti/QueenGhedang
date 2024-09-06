import json
import datetime
import urllib.request
from django.conf import settings

from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Kategori, Kontak, Profil, Slide, Statis, Custumer, ChatID
from cart.models import Transaksi, DetailTransaksi, Tracking
from django.db.models import Count
from django.core.paginator import Paginator
from django.views.generic import View
from django.contrib import messages
from django.db.models import Q
from cart.keranjang import Cart
from cart.forms import CartAddProductForm

from administrator.forms import CustumerForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group

from .telegram_utill import send_telegram_message
from django.contrib.humanize.templatetags.humanize import intcomma

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .decorators import tolakhalaman_ini, ijinkan_pengguna

from django.views.decorators.csrf import csrf_exempt
from .constants import PAYMENT_STATUS
import midtransclient
import uuid
import datetime


snap = midtransclient.Snap(
    is_production=False,
    server_key='SB-Mid-server-2TTrDPjbHAoYs84Ly1nyCfjO',
    client_key='SB-Mid-client-igWEof-450nDMO6l',
)

def beranda(request):
    jumlahkategori = Kategori.objects.all().annotate(product_count=Count('produks')).order_by('-id')
    slider = Slide.objects.filter(aktif=True).order_by('-id')
    baru = Product.objects.filter(keterangan_barang="Baru")
    makanan = Product.objects.filter(menu='MAKANAN')
    minuman = Product.objects.filter(menu='MINUMAN')
    product = Product.objects.order_by('-id')
    context = {
            "judul" : "Beranda",
            "jumlahkategori" : jumlahkategori,
            "slide": slider,
            "baru":baru,
            "minuman":minuman,
            "product":product,
            "makanan" : makanan,
    }
    return render(request, 'beranda.html', context)

def profil(request):
    profil = Profil.objects.all().order_by('-id')[:1]
    context = {
        "judul": "Profil",
        "profil":profil,
    }
    return render(request, 'profil.html', context)

def kategori(request, slug):
    kategori = get_object_or_404(Kategori, slug=slug)
    produk =  kategori.produks.order_by('-id')
    jmlproduk = Product.objects.filter(kategori=kategori).count()
    halaman_tampil = Paginator(produk, 8)
    halaman_url = request.GET.get('halaman',1)
    halaman_produk = halaman_tampil.get_page(halaman_url)
    if halaman_produk.has_previous():
        url_previous = f'?halaman={halaman_produk.previous_page_number()}'
    else:
        url_previous = ''

    if halaman_produk.has_next():
        url_next = f'?halaman={halaman_produk.next_page_number()}'
    else:
        url_next = ''
    context = {
         "judul": "Kategori",
         "detailkategori": kategori,
         "produk" : halaman_produk,
         "previous" : url_previous,
          "next" : url_next,
          "jmlproduk":jmlproduk,
    }
   
    return render(request, 'kategori.html', context)

def product(request, kategori_slug, slug):
    produk = get_object_or_404(Product, slug=slug)
    related = Product.objects.filter(kategori=produk.kategori.id)
    jml = related.count()
    cart_product_form = CartAddProductForm()
   
    context = {
         "judul": "Product",
         "produk":produk,
         "related":related,
         "jml":jml,
        "cart_product_form": cart_product_form,
       
    }
    return render(request, 'product.html', context)

class KontakView(View):
    def get(self, request):
        context = {
        'judul': ' Kontak',
       }
        return render(request, 'kontak.html', context)
       
    def post(self, request):
        context = {
            'judul': ' Kontak',
            'data': request.POST,
            'has_error': False
        }
        nama = request.POST.get('nama')
        no_whatsup = request.POST.get('whatsapp')
        subject = request.POST.get('subject')
        email = request.POST.get('email')
        pesan = request.POST.get('pesan')
        if nama=="":
           messages.error(request, 'Nama Masih kosong')
           context['has_error'] = True

        if no_whatsup=="":
               messages.error(request, 'No whatsapp Masih kosong')
               context['has_error'] = True

        if subject=="":
               messages.error(request, 'Subject Masih kosong')
               context['has_error'] = True

        if pesan=="":
               messages.error(request, 'Pesan Masih kosong')
               context['has_error'] = True

        if context['has_error']:
            return render(request, 'kontak.html', context, status=400)

        kontak = Kontak.objects.create(nama = nama, email = email, no_whatsup=no_whatsup, subject = subject,  isi = pesan )
        kontak.save()
        context = {
                    'judul': 'Kontak',
                    'data': "",
                    'has_error': False
        }
        messages.success(request, 'Pesan sudah terkirim, silakan tunggu respon selanjutnya!')
        return render(request, 'kontak.html', context, status=400)
    
class CheckoutView(View):
   
    def get(self , request , *args , **kwargs):
        # bank = Bank.objects.order_by('-id')
        context = {
        'judul': 'Checkout',
        # 'bank':bank,
       }
        return render(request, 'checkout.html', context)
      
    def post(self , request , *args , **kwargs):
        id_konsumen = request.user.custumer.id
        konsumen = Custumer.objects.get(id=id_konsumen)
        # bank = Bank.objects.order_by('-id')
        context = {
            'judul': 'checkout',
            'data': request.POST,
            'has_error': False,
            # 'bank':bank,
          
        }
        grantotal = request.POST.get('grantotal')
        tujuan = request.POST.get('tujuan')
        # jam_book = request.POST.get('jam_book')
        alamat_kirim = request.POST.get('alamat_kirim')
        wa_kirim = request.POST.get('wa_kirim')

        no_transaksi = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        if grantotal == "0" :
            messages.error(request, 'Anda belum berbelanja, Silakan belanja terlebih dahulu')
            context['has_error'] = True
        if tujuan == "0" :
           messages.error(request, 'Silakan isi terlebih dahulu Tujuan Makanan')
           context['has_error'] = True

        if context['has_error']:
                return render(request, 'checkout.html', context, status=400)
       
      
        if tujuan == "ditempat" :
            if context['has_error']:
                return render(request, 'checkout.html', context, status=400)

            transaksi = Transaksi.objects.create(no_transaksi = no_transaksi, 
                                        keterangan_pesanan = tujuan,
                                        custumer = konsumen,
                                        total_transaksi = grantotal )
            transaksi.save()
            keranjang = Cart(request)
            for r in keranjang:
                
                instance_detail= DetailTransaksi(
                    no_transaksi = no_transaksi,
                    product = r['product'],
                    jumlah = r['quantity'],
                )
                instance_detail.save()

                dibeliupdate=Product.objects.get(nama_produk=r['product'])
                dibeliupdate.dibeli+=int(r['quantity'])
                dibeliupdate.save()
                
                chats = ChatID.objects.filter(aktif=True)
                for chat in chats:
                        grantotal_formatted = f"Rp. {intcomma(grantotal)}"
                        message = f"Assalamualaikum Wr Wb,\n\nNo Transaksi: <b>{no_transaksi}</b>\nKeterangan_pesanan: <b>{tujuan}</b>\nCustumer: <b>{konsumen}</b>\nTotal Transaksi: <b>{grantotal}</b>\n\nTerimakasih, Salam Queen Ghedang Store dan Wassalamualaikum Wr Wb."
                        send_telegram_message(chat.chatid, message)
                
                
            keranjang.clear()
            messages.success(request, 'Silakan bayar dengan menggunakan VA virtual Account dengan benar dan baik')
            return redirect('histori')  

        if tujuan == "dilokasi" :
                
        
                transaksi = Transaksi.objects.create(no_transaksi = no_transaksi, 
                                                    keterangan_pesanan = tujuan,
                                                    custumer = konsumen,
                                                    alamat_kirim = alamat_kirim,
                                                    wa_kirim = wa_kirim,
                                                    total_transaksi = grantotal)
                transaksi.save()
                keranjang = Cart(request)
                for r in keranjang:
                            
                    instance_detail= DetailTransaksi(
                        no_transaksi = no_transaksi,
                        product = r['product'],
                        jumlah = r['quantity'],
                    )
                    instance_detail.save()

                    dibeliupdate=Product.objects.get(nama_produk=r['product'])
                    dibeliupdate.dibeli+=int(r['quantity'])
                    dibeliupdate.save()

                    chats = ChatID.objects.filter(aktif=True)
                    for chat in chats:
                            grantotal_formatted = f"Rp. {intcomma(grantotal)}"
                            message = f"Assalamualaikum Wr Wb,\n\nNo Transaksi: <b>{no_transaksi}</b>\nKeterangan_pesanan: <b>{tujuan}</b>\nCustumer: <b>{konsumen}</b>\nAlamat_kirim: <b>{alamat_kirim}</b>\nWa_kirim: <b>{wa_kirim}</b>\nTotal Transaksi: <b>{grantotal}</b>\n\nTerimakasih, Salam Queen Ghedang Store dan Wassalamualaikum Wr Wb."
                            send_telegram_message(chat.chatid, message)
                        
                keranjang.clear()
                messages.success(request, 'Silakan bayar dengan menggunakan VA virtual Account dengan benar dan baik')
                return redirect('histori')

def logoutpage(request):
    logout(request)
    return redirect('loginpage')

@tolakhalaman_ini
def loginpage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user_obj = User.objects.filter(username = username).first()
        if user_obj is None:
            messages.error(request, 'Username Tidak ditemukan')
            return redirect('loginpage')
        
        cocokan = authenticate(request, username=username, password=password)
        if cocokan is None:
            messages.error(request, 'Usernama dana Password yang anda masukan salah')
            return redirect('loginpage')
        if cocokan is not None:
            login(request, cocokan)
            return redirect('beranda_admin')
    context = {
        'judul': 'Login',
    }
    return render(request, 'login.html', context)

@tolakhalaman_ini
def register(request):
    form = CustumerForm()
    if request.method == "POST":
        
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        user = User.objects.create_user(username=username, email=email)
        user.set_password(password)
        user.is_active = True
        user.save()

        akses_custumer = Group.objects.get(name='custumer')
        user.groups.add(akses_custumer)
        formsimpan = CustumerForm(request.POST)
        if formsimpan.is_valid():
            register = formsimpan.save()
            register.user = user
            register.save()
            return redirect('loginpage')
    context = {
        'judul': 'Register',
        'form':form
    }
    return render(request, 'register.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['custumer']) 
def histori(request):
    id_konsumen = request.user.custumer.id
    konsumen = Custumer.objects.get(id=id_konsumen)
    tempat = Transaksi.objects.filter(keterangan_pesanan="ditempat" , custumer=konsumen.id).order_by('-id')
    lokasi = Transaksi.objects.filter(keterangan_pesanan="dilokasi" , custumer=konsumen.id).order_by('-id')
    transaksi = Transaksi.objects.filter(custumer__id=id_konsumen).order_by('-id')
    context = {
        "judul": "Histori",
        "tempat":tempat,
        "lokasi":lokasi,
        "transaksi":transaksi

       
    }
    return render(request, 'histori.html', context)

def cari(request):
       
    datakata=request.GET.get('kata')
    if request.method == 'GET':
        search_query = request.GET.get('kata', None)
        if search_query:
            hasilcari = Product.objects.filter(nama_produk__icontains=datakata).order_by('-id')
   
        
    cart_product_form = CartAddProductForm()
    jmlproduk = hasilcari.count()
    context = {
        "judul": "Cari",
        "cart_product_form": cart_product_form,
        "hasilcari": hasilcari,
        "jmlproduk":jmlproduk
    }
   
    return render(request, 'cari.html', context)



def isivitual(request, notransaksi):
    transaksi = Transaksi.objects.get(no_transaksi=notransaksi)
    token_payment = uuid.uuid4().hex 
    detail = DetailTransaksi.objects.filter(no_transaksi=notransaksi)
    transaksi.token_payment = token_payment
    transaksi.save()
    item_details = []
    for row in detail:
        item_detail = {
            'id': row.id,
            'price': row.harga,
            'quantity': row.jumlah,
            'name': row.product.nama_produk,
        }
        item_details.append(item_detail)
    transaction_details = {
        # 'order_id': uuid.uuid4().hex,
        'order_id': token_payment,
        'gross_amount': transaksi.total_transaksi,
    }
    custumer_details = {
        'first_name': transaksi.custumer.nama,
        'email': transaksi.custumer.email,
        'phone':transaksi.custumer.wa,
    }
    transaction_data = {
        'transaction_details': transaction_details,
        'item_detail': item_detail,
        'custumer_details': custumer_details,
       
    }
  
    response = snap.create_transaction(transaction_data)

    transaction_token = response['token']
    transaction_redirect_url = response['redirect_url']

    context = {
        "judul": "Halaman Payment Gateway",
         'url':transaction_redirect_url,
         'token':transaction_token,
          'transaksi':transaksi,
        'detail':detail
    }
    return render(request, 'va.html', context)

@csrf_exempt
def midtrans_callback(request):
    if request.method == 'POST':
        # Ambil data callback dari Midtrans
        data = request.POST['result_data']
        hasil = json.loads(data)
        print(hasil)

        order_id = hasil['order_id']
        print(order_id)
        
        transaction_status = PAYMENT_STATUS[hasil['transaction_status']]
        transaction = Transaksi.objects.get(token_payment=order_id)
        transaction.status = transaction_status
        transaction.save()

        # Lakukan tindakan tambahan sesuai kebutuhan aplikasi, contoh:
        if transaction_status == 'Lunas':

            detailtransaksi = DetailTransaksi.objects.values('jumlah','product__id').filter(no_transaksi=transaction.no_transaksi)
            for detail in detailtransaksi:
                product = Product.objects.get(id=detail['product__id'])
                product.stock -= detail['jumlah']
                product.dibeli += detail['jumlah']
                product.save()
          

    # Jika request bukan POST, kembalikan respons 400 (Bad Request)
    context = {
         "judul": "Halaman Keterangan Payment Gateway", 
        'pesan':hasil['status_message'],
       

         
     
    }
    return render(request, 'hasilva.html', context)

@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['custumer'])   
def tracking(request):
    id_konsumen = request.user.custumer.id
    konsumen = Custumer.objects.get(id=id_konsumen)
   
    lokasi = Transaksi.objects.filter(keterangan_pesanan="dilokasi" , custumer=konsumen.id).order_by('-id')
    
    context = {
        "judul": "Tracking",
        "lokasi":lokasi 
    }
  
    return render(request, 'tracking.html', context)  


@login_required(login_url='loginpage')
@ijinkan_pengguna(yang_diizinkan=['custumer'])   
def trackingantar(request, transaksi):
    id_transaksi = Transaksi.objects.get(no_transaksi=transaksi)
    track = Tracking.objects.filter(transaksi=id_transaksi.id).order_by('-id')
    
    context = {
        "judul": "Hasil Tracking Transaksi ke Lokasi",
        "track":track,
        "id_transaksi":id_transaksi
    }
  
    return render(request, 'hasiltracking.html', context) 



def kategoriberanda(request):
    kategori = Kategori.objects.filter(aktif=True).order_by('-id')
    return {'kategori':kategori}

def modalberita(request):
    modalproduk = Product.objects.order_by('-id')
    return {'modalproduk':modalproduk}

def statisweb(request):
    statis = Statis.objects.get(id=1)
    return {'statis':statis}