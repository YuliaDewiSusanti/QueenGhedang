# Generated by Django 5.0.6 on 2024-06-20 09:34

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('website', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaksi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_transaksi', models.CharField(max_length=200, null=True)),
                ('wa_kirim', models.CharField(blank=True, max_length=200, null=True, verbose_name='No Whatsapp')),
                ('alamat_kirim', models.CharField(blank=True, max_length=300, null=True)),
                ('total_transaksi', models.BigIntegerField(blank=True, null=True)),
                ('keterangan_pesanan', models.CharField(blank=True, choices=[('ditempat', 'ditempat'), ('dilokasi', 'dilokasi')], max_length=200, null=True)),
                ('status', models.CharField(blank=True, choices=[('Belum Lunas', 'Belum Lunas'), ('Lunas', 'Lunas'), ('Pengiriman', 'Pengiriman'), ('Selesai', 'Selesai'), ('Gagal', 'Gagal'), ('Kadaluarsa', 'Kadaluarsa'), ('Pembayaran Ditolak', 'Pembayaran Ditolak')], default='belum lunas', max_length=200, null=True)),
                ('date_created', models.DateTimeField(auto_now_add=True, null=True)),
                ('token_payment', models.CharField(blank=True, max_length=300, null=True)),
            ],
            options={
                'verbose_name_plural': 'Transaksi',
            },
        ),
        migrations.CreateModel(
            name='DetailTransaksi',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('no_transaksi', models.CharField(max_length=200, null=True)),
                ('jumlah', models.IntegerField(blank=True, null=True)),
                ('product', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='website.product')),
            ],
            options={
                'verbose_name_plural': 'Detail Transaksi',
            },
        ),
    ]
