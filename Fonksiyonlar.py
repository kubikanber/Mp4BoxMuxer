# Mp4BoxMuxer
# Ana kod içersinde tekrarlayan kodlar
# için fonksiyon oluşturulmuştur ve burada tanımlanmıştır.

import gettext


# Verilen dosya ismi ve dosya yolunda ilgili .mo dosyasının olup olmadığını konroletmek için
# Dosya var ise dosya yolu ile
# Yok ise None ile dönüş yapar.
# @mo_dosyası: str
# @return
def dil_dosyası_kontrol(mo_dosyası: str, dil_klasör_yolu: str, dil: []):
    dil_varmı = gettext.find(mo_dosyası, localedir=dil_klasör_yolu, languages=dil)
    return dil_varmı
