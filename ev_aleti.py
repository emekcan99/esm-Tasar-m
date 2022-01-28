import pandas as pd
data='data.xlsx'
df=pd.read_excel(data,index_col=0)
a=df.loc[:, 'Aylık Tüketim (kWh)']
toplamKWatt=(a.sum())/30
toplamKWatt=round(toplamKWatt)
haftalikKullanim=df.loc[:,'Haftada Kaç Defa Kullanılıyor?']
gunlukCalismaSuresi=df.loc[:,'Günlük Çalışma Süresi(Saat)']
anlikTuketim=df.loc[:,'Tüketim (W)']


def panelAdedi(toplamKWatt):
    gunlukGuneslenme=float(input("lütfen kurulacak ilin en düşük güneşlenme süresini giriniz"))
    panelKapasite=toplamKWatt/gunlukGuneslenme
    secilenPanel=float(input("seçtiğiniz panelin saatlik ürettiği gücü giriniz"))
    panelAdeti=((panelKapasite*1000)/secilenPanel)*0.8
    panelAdeti=round(panelAdeti)
    print("kurmanız gereken panel adedi {} tanedir".format(panelAdeti))
    return panelAdeti
def regulator(panelAdedi):
    p=float(input("lütfen paralel bağlanacak panel adedini giriniz toplam panel adediniz {}".format(panelAdedi)))
    s = int(input("lütfen seri bağlanacak panel adedini giriniz toplam panel adediniz {}".format(panelAdedi)))
    v=float(input("lütfen seçtiğiniz güneş panelinin ürettiği gerilim değerini giriniz"))
    a=float(input("lütfen seçtiğiniz güneş panelinin ürettiği akım değerini giriniz"))
    if panelAdedi%2==0:
        uretilenAkim=(panelAdedi/s)*a
        uretilenV=(panelAdedi/p)*v
        print("seçmeniz gereken regulator {}A değerinde olmalı".format(uretilenAkim))
    elif panelAdedi%2!=0:
        y=input("artan paneli seri bağlamak için 1 paralel bağlamak için 2 ye basınız ")
        if y=="1":
            uretilenAkim = (panelAdedi / s) * a
            uretilenV = (panelAdedi / p) * v
            uretilenV=uretilenV+v
            print("seçmeniz gereken regulator {}A değerinde olmalı".format(uretilenAkim))
        elif y=="2":
            uretilenAkim = (panelAdedi / s) * a
            uretilenV = (panelAdedi / p) * v
            uretilenAkim=uretilenAkim+a
            print("seçmeniz gereken regulator {}A değerinde olmalı".format(uretilenAkim))


def akuAdet(toplamKWatt):
    bulutlulukFaktor=float(input("lütfen kurmak istediğiniz ilin bulutluluk faktorünü giriniz"))
    akuVerim=float(input("lütfen seçilen akünün şarj verimliliğini giriniz"))
    kGaG=(toplamKWatt*bulutlulukFaktor)/(akuVerim*0.8)
    akuAh=float(input("lütfen belirlediğiniz akünün ah değerini giriniz"))
    akuV=float(input("lütfen belirlediğiniz akünün V değerini giriniz "))
    aG=akuV*akuAh
    aG=aG/1000
    bA=kGaG/aG
    bA=round(bA)
    print("kurmanız gereken akü adedi {} tanedir ".format(bA))
    return bA
def inverter(haftalikKullanim,gunlukCalismaSuresi,anlikTuketim):
    haftalikKullanimL=[]
    gunlukCalismaSuresiL=[]
    kullanilmaSuresi=[]
    anlikTuketimL=[]
    enCokKullanilan=[]
    sayac=0
    sayac2=0
    sayac3=0
    index=[]
    enCokWatt=[]
    toplam=0
    for i in haftalikKullanim:
        haftalikKullanimL.append(i)
        sayac=sayac+1
    for i in gunlukCalismaSuresi:
        gunlukCalismaSuresiL.append(i)
    for i in anlikTuketim:
        anlikTuketimL.append(i)
    for i in range(sayac):
        kullanilmaSuresi.append(haftalikKullanimL[i]*gunlukCalismaSuresiL[i])
    for i in kullanilmaSuresi:
        if i>9:
            enCokKullanilan.append(i)
            index.append(sayac2)
        sayac2 = sayac2 + 1

    for i in anlikTuketimL:
        for j in index:
            if sayac3==j:
                enCokWatt.append(i)

        sayac3=sayac3+1
    for i in enCokWatt:
        toplam=toplam+i
    enYuksekTuketim = max(anlikTuketimL)
    toplam=toplam+enYuksekTuketim
    inv=toplam*1.5
    print("seçmeniz gereken inverter {} watt tır e %10 altında seçilebilir".format(inv))
    return inv


def maliyet(panelAdeti,bA,a):
    enf=(0.15)/12
    tKW=0
    amorti = 0
    sP=int(input("lütfen seçtiğiniz panelin fiyatını giriniz"))
    b=int(input("lütfen seçmiş olduğunuz akünün fiyatını giriniz"))
    reg=int(input("lütfen seçmiş olduğunuz regülatörün fiyatını giriniz "))
    i=int(input("lütfen seçmiş olduğunuz inverter fiyatını giriniz"))
    kM=int(input("lütfen kalan maliyetleri giriniz işçilik kablo konnektör vb..."))
    m=sP*panelAdeti+b*bA+reg+i+kM
    print("şuanki maliyetiniz {}tl".format(m))

    e=float(input("lütfen bölgedeki elektrik kW/H fiyatnı giriniz"))
    for i in a:
        tKW=tKW+i
    aM=e*tKW
    print("şuanki aylık elektrik maliyetiniz {}".format(aM))
    while m>=0:
        m=m-aM
        aM=(aM*enf)+aM
        amorti=amorti+1
    amortiY=amorti/12
    amortiA=amorti%12
    print("kurulan sistem kendini {} yıl {} ay da amorti eder".format(round(amortiY),amortiA))




print("""
****************************************************************************
off grid güneş paneli kurulumu ve maliyeti hesaplama programına hoş geldiniz
lütfen başarılı bir sonuç için istenilen bilgileri eksiksiz giriniz
öncelikle ev içerisinde bulunan ev aletlerini ve kullanılma sürelerini bir excel
dosyası halinde programın bulunduğu klasöre atmanız gerekir
*****************************************************************************""")
panelAdeti=panelAdedi(toplamKWatt)
bA=akuAdet(toplamKWatt)
regulator(panelAdeti)
inv=inverter(haftalikKullanim,gunlukCalismaSuresi,anlikTuketim)
maliyet(panelAdeti,bA,a)