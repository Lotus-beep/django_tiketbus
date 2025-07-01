import json
from datetime import datetime, timedelta

from django.shortcuts import render
from django.contrib.auth.models import User
from .function import Kalkulate,CreateKode
from .models import Profile,Tiketbus,TypeTiket,PesananTiket
from .serializer import *

from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView

class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            response = super().post(request, *args, **kwargs)
            token = response.data

            AccesToken = token['access']
            refrestoken = token['refresh']

            res = Response()
            res.data = {'success':True}

            res.set_cookie(
                key='access_token',
                value=AccesToken,
                httponly=True,
                max_age=3600 * 3,
                secure=True,
                samesite="None",
                path='/'
            )

            return res
        
        except:
            return Response()
        

class CustemRefresTokenView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refesh_token = request.COOKIES.get('refresh_token')
            request.data['refresh'] = refesh_token
            response = super().post(request, *args, **kwargs)
            tokens = response.data
            acces_token = tokens['access']
            res = Response()
            res.data = {'refreshed':True}
            
            res.set_cookie(
                key='access_token',
                value= acces_token,
                max_age=10800,
                httponly=True,
                secure=True,
                samesite="None",
                path='/'
            )

            return res

        except:
            return Response({'refreshed':False})


@api_view(['GET'])
def logout(request):
    try:
        res = Response()
        res.data = {'success':True}
        res.delete_cookie('access_token',path='/',samesite="None")
        res.delete_cookie('refresh_token',path='/',samesite="None")
        return res
    except:
        Response({'success':False})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def is_authenticated(request):
    return Response({'Aunthenticated':True})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gettiket(request):
    getdata = Tiketbus.objects.all()
    Serializers = JadwalBusserialazers( getdata,many=True )
    return Response(Serializers.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def gettiketid(request,id):
    getdata = TypeTiket.objects.filter(tiketbus=id)
    Serializers = TypeTiketserialazers( getdata,many=True )
    return Response(Serializers.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreateTypeTiket(request):
    kode = []
    tiketbus_id = request.data.get('tiketbus')
    getbus = Tiketbus.objects.filter(id=tiketbus_id).first()
    if not getbus:
        return Response({'error': 'Tiketbus tidak ditemukan'}, status=500)

    array_data = request.data.get('no_bangku', [])
    if not isinstance(array_data, list) or not array_data:
        return Response({'error': 'Data bangku tidak valid'}, status=500)

    if getbus.jumlah_bangku < len(array_data):
        return Response({'error': 'Jumlah bangku tidak mencukupi'}, status=500)

    for no_bangku in array_data:
        kode_tiket = CreateKode('typetiket')
        getdata = {
            'tiketbus': tiketbus_id,
            'no_bangku': no_bangku,
            'type_tiket': request.data.get('type_tiket'),
            'kode_tiket': kode_tiket,
            'status': False,
            'user': request.user.id,
        }
        serializer = CreateTiketSerializer(data=getdata)
        if serializer.is_valid():
            serializer.save()
            kode.append(kode_tiket)
        else:
            print(serializer.errors)
            return Response(serializer.errors)

    getbus.jumlah_bangku -= len(array_data)
    getbus.save()

    response = Response({'success': 'succes'}, status=200)
    tiket_data = json.dumps({'kodetiket': kode})

    response.set_cookie(
        key='kode_tiket',
        value=tiket_data,
        max_age=3600,
        secure=True,  
        httponly=True,
        samesite='None',
        path='/'
    )

    return response



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def CreatePesanan(request): 
    cookies = request.COOKIES.get('kode_tiket')
    if not cookies:
        return Response({'error': 'Maaf token pembayaran anda sudah expired silahkan memesan lagi'}, status=404)

    parse = json.loads(cookies)

    data_array = parse['kodetiket']

    now = datetime.now()

    tanggal = now.strftime("%d-%m-%Y")   
    waktu = now.strftime("%H:%M")     

    getdata = {
        'tiketbus': request.data.get('tiketbus'),
        'typetiket': request.data.get('typetiket'),
        'total_pemesanan':request.data.get('total_pemesanan'),
        'user_payment':request.data.get('user_payment'),
        'waktu':waktu,
        'tanggal':tanggal
        }
    print('hello')
    print(parse)
    print(data_array)
    Validate = Kalkulate(getdata['total_pemesanan'],getdata['typetiket'],int(getdata['user_payment']))
    kode_pesanan = CreateKode('pesanan')
    kode = json.dumps({'kode':kode_pesanan})
    waktu = getdata['waktu']
    tanggal = getdata['tanggal']
    
    if Validate:
        for data in data_array:
            print(kode_pesanan)
            data_pesanan = {
                'tiketbus': getdata['tiketbus'],
                'kode_tiket': data,
                'user': request.user.id,
                'kode_pesanan': kode_pesanan,
                'tanggal':tanggal,
                'waktu':waktu
            }
            Serializers = CreatePesananSerializer(data = data_pesanan)
            if Serializers.is_valid():
                Serializers.save()
            else:
                return Response(Serializers.errors)
            
        for data in data_array:
            content = TypeTiket.objects.filter(kode_tiket=data).first()
            content.status = True
            content.save()
            
        response = Response({'succes':'Pesanan berhasil di simpan'})

        response.delete_cookie('kode_tiket',path='/',samesite="None")

        response.set_cookie(
            key='kode_pesanan',
            value=kode,
            max_age=3600,
            secure=True,  
            httponly=True,
            samesite='None',
            path='/'
        )
        return response
    else:
        return Response({'error': 'Maaf dana anda tidak mencukupi'}, status=404)



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_notes(request):
    user = request.user
    notes = Profile.objects.filter(user=user)
    TypeTiket.objects.filter(user=user,status=False).delete()
    seriliazer = Noteserialazers(notes, many=True)
    return Response(seriliazer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_tiket(request):
    cookies = request.COOKIES.get('kode_pesanan')
    kode = json.loads(cookies)
    notes = PesananTiket.objects.filter(kode_pesanan=kode['kode'])
    seriliazer = CetaktiketSerializers(notes, many=True)
    res = Response(seriliazer.data)
    res.delete_cookie('kode_pesanan',path='/',samesite="None")
    return Response(seriliazer.data)


@api_view(['POST'])
@permission_classes([AllowAny])
def Register(request):
    Serializers = UserRegisterSerializer(data = request.data)
    if Serializers.is_valid():
        Serializers.save()
        return Response({'success':True})
    return Response(Serializers.errors)


