import random
from .models import TypeTiket,PesananTiket

def handle_type(type):
    print(type)
    match type:
        case "Reguler":
            return 100000
        case "Executiv":
            return 500000
        case _:  
            return 0


def Kalkulate(Total,Type,Payment):
    Price = Total * handle_type(Type)
    kalkulate = Payment - Price
    print(kalkulate)
    if kalkulate >= 0 :
        return True
    else:
        return False
        
def CreateKode(model):
    while True:
        random_number = random.randint(100, 999)
        data = "DEDASFDCW" if model == "pesanan" else "qwyteydg2"
        kodetiket = data + str(random_number)
        if not TypeTiket.objects.filter(kode_tiket=kodetiket).exists():
            return kodetiket
        
        