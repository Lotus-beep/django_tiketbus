from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    no_telpon = models.CharField(max_length=12, null=True, blank=True)
    description = models.CharField(max_length=100, null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='profile') 

class Tiketbus(models.Model):
    type = models.CharField(max_length=8)
    jumlah_bangku = models.PositiveSmallIntegerField()
    jurusan = models.CharField(max_length=30)
    waktu_berangkat = models.TimeField(null=True, blank=True)

class TypeTiket(models.Model):  
    tiketbus = models.ForeignKey(Tiketbus, on_delete=models.CASCADE, related_name='tiket')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='type_tikets')  # ✅ unique name
    no_bangku = models.IntegerField()
    type_tiket = models.CharField(max_length=8)
    kode_tiket = models.CharField(max_length=12, unique=True)
    status = models.BooleanField()

class PesananTiket(models.Model):
    tiketbus = models.ForeignKey(Tiketbus, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='pesanan_tikets')  # ✅ unique name
    kode_tiket = models.ForeignKey(
        TypeTiket,
        to_field='kode_tiket',
        on_delete=models.CASCADE,
        related_name='pesanan'
    )
    tanggal = models.CharField(max_length=10)
    waktu = models.TimeField(null=True, blank=True)
    kode_pesanan = models.CharField(max_length=12)
