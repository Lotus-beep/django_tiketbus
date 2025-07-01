from rest_framework import serializers
from . models import *

class Noteserialazers(serializers.ModelSerializer):
    class Meta:
        model=Profile
        fields = ['id', 'description']

class JadwalBusserialazers(serializers.ModelSerializer):
    class Meta:
        model=Tiketbus
        fields = ['id', 'type','jumlah_bangku','jurusan','waktu_berangkat']

class TypeTiketserialazers(serializers.ModelSerializer):
    class Meta:
        model=TypeTiket
        fields = ['no_bangku','status']

class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields = ['username']

class UserRegisterSerializer(serializers.ModelSerializer):
    Password = serializers.CharField(write_only=True)
    class Meta:
        model=User
        fields = ['username','email','Password']

    def create(self, validated_data):
        user = User(
            username=validated_data['username'],
            email=validated_data['email']
        )
        user.set_password(validated_data['Password'])
        user.save()
        return user
    
class CreateTiketSerializer(serializers.ModelSerializer):
    class Meta:
        model= TypeTiket
        fields = ['tiketbus','user','no_bangku','type_tiket','kode_tiket','status']

    def create(self, validated_data):
        typeTiket = TypeTiket(
            tiketbus=validated_data['tiketbus'],
            user=validated_data['user'],
            no_bangku=validated_data['no_bangku'],
            type_tiket=validated_data['type_tiket'],
            kode_tiket=validated_data['kode_tiket'],
            status=validated_data['status']
        )
        typeTiket.save()

        return typeTiket
    
class CreatePesananSerializer(serializers.ModelSerializer):
    class Meta:
        model= PesananTiket
        fields = ['tiketbus','user','kode_tiket','tanggal','waktu','kode_pesanan']

    def create(self, validated_data):
        addPesanan = PesananTiket(
            tiketbus=validated_data['tiketbus'],
            user=validated_data['user'],
            kode_tiket=validated_data['kode_tiket'],
            tanggal=validated_data['tanggal'],
            waktu=validated_data['waktu'],
            kode_pesanan=validated_data['kode_pesanan']
        )
        addPesanan.save()

        return addPesanan

class CetaktiketSerializers(serializers.ModelSerializer):
    pesanan_tikets = serializers.CharField(source='user.username')
    tiketbus = serializers.CharField(source='tiketbus.jurusan')
    no_bangku = serializers.IntegerField(source='kode_tiket.no_bangku')
    type_tiket = serializers.CharField(source='kode_tiket.type_tiket')
    waktu_berangkat = serializers.CharField(source='tiketbus.waktu_berangkat')
    class Meta:
        model=PesananTiket
        fields = ['pesanan_tikets','no_bangku','tiketbus','kode_pesanan','tanggal','type_tiket','waktu','waktu_berangkat']