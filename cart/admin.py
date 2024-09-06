from django.contrib import admin
from django.db import models
from .models import Transaksi, DetailTransaksi, Tracking
from django.utils.html import format_html

class TransaksiAdmin(admin.ModelAdmin):
    def tanggal_pesan(self, obj):
        return obj.date_created.strftime("%d %b %Y %H:%M:%S")
    
    def show_firm_url(self, obj):
        return format_html("<a href='https://api.whatsapp.com/send?phone={url}&text=Apakah%20anda%20telah%20memesan%20produk%20di%20Tani%20Jaya?' target='_blank'>{url}</a>", url=obj.whatsapp)
    show_firm_url.short_description = "Hubungi"

    def selengkapnya(self,obj):
        
        return format_html("<a href='http://localhost:8000/admin/cart/detailtransaksi/?no_transaksi={trans}'>{trans}</a>", trans=obj.no_transaksi)
    selengkapnya.short_description = "Detail Pesan" 
    readonly_fields = ["no_transaksi","total_transaksi"]
    list_filter = ['status']


class DetailTransaksiAdmin(admin.ModelAdmin):
    list_display = ['no_transaksi','product','harga','jumlah','sub_total']
    list_filter = ['no_transaksi']
    readonly_fields = ["no_transaksi","product","jumlah"]
    def has_add_permission(self, request):
        return False
   
    
    def render_change_form(self, request, context, add=False, change=False, form_url='', obj=None):
        context.update({
            'show_save': False,
            'show_save_and_continue': False,
            'show_delete': False
        })
        return super().render_change_form(request, context, add, change, form_url, obj)

admin.site.register(Transaksi, TransaksiAdmin)
admin.site.register(DetailTransaksi, DetailTransaksiAdmin)
admin.site.register(Tracking)

