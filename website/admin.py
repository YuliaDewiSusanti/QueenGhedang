from django.contrib import admin
from django.db import models
from django.forms import TextInput
from .models import Kategori,Product, Kontak, Profil, Slide, Statis, Custumer, ChatID

class KategoriAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('nama',)} 
    
class KontakAdmin(admin.ModelAdmin):
    list_display = ['nama','no_whatsup','subject','email']
class SlideAdmin(admin.ModelAdmin):
    list_display = ['judul']   
class ProductAdmin(admin.ModelAdmin):
    list_display = ['nama_produk','kategori','no_whatsup']
    prepopulated_fields = {'slug': ('nama_produk',)} 
    readonly_fields = ["dibeli"]
    formfield_overrides = {
        models.PositiveIntegerField: {'widget': TextInput(attrs={'size':'20'})},
        models.PositiveBigIntegerField: {'widget': TextInput(attrs={'size':'25','placeholder':'628##########'})},
        models.CharField: {'widget': TextInput(attrs={'size':'70' })},
    }

class StatisAdmin(admin.ModelAdmin):
    pass
class ProfilAdmin(admin.ModelAdmin):
   
    pass

admin.site.register(Kategori, KategoriAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Kontak,KontakAdmin)
admin.site.register(Profil, ProfilAdmin)
admin.site.register(Slide,SlideAdmin)
admin.site.register(Statis, StatisAdmin)
admin.site.register(Custumer)
admin.site.register(ChatID)


