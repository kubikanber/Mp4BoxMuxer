# !/usr/bin/env python3
# Bu program türkçe yazılmıştır. All names given Turkish
# Log alma işi tüm basamaklarda ayrıntısına kadar log dosyasına aktarılacak. Çoklu dili destekleyecek.
# çok dilli uygulama halinde olacak ilk tanımlı olan türkçe olacak sonra eng
# çok lu dil özelliği için kurulmuş olan dil klasörleri kontrol edilecek yok ise eng ye dönecek bir mekanizma yapılacak

# 1. komut argumanları ve özelikleri yapılacak.
# komut argümanları dil çevirme özellikleri yapıldı.
#       en ve tr loceles klasörü oluşturulup, içersine .po ve mo dosyaları uygun klasör yolları ile konuldu.
# sistem hangi bölgede olduğu alınıp ona göre dil harfı ve kodlaması alındı.
# kullanılacak olan MP4Box kütüphanesi sistemde kurulu konrolu yapılcak yok ise bunun için bir mekanizma
# MP4Box için argümanlar tamımlanacak
# ilk argüman "info"
#  örnek: Mp4Muxer input.m* -i (--info) kommutu veridiğinde, medya dosyasının özellikleri verilecek.
#   Dosya çıktısı için:
#       daha sonra benim belirdeğim öntanımlı şekle göre çıkış dosyası aynı yere sonuna mux elenerek yaratılacak, aynı
#       isimde dosya var ise isminin sonuna sayı eklenecek.

import logging
import argparse
import gettext
import locale
import os
from Fonksiyonlar import *

_ = gettext.gettext
öntanımlı_diller = ["en", "tr"]

# kayıt işlemleri; logging. Basit bir log çıktısı için.
logging.basicConfig(filename="Mp4BoxMuxer.log",
                    filemode="w",
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s: %(message)s")
logging.info(_("Program başlıyor. Log tanımlamaları yapıldı."))
# log dosyası için kod içersinde gerekli ayarlamalar yapılacak

# Kullanılan dilini belirleme
kullanıcı_dilini_bul = locale.getdefaultlocale()
logging.debug(_("Yerel dil ve kodu alındı.: %s"), kullanıcı_dilini_bul)
sistem_dili = " (" + kullanıcı_dilini_bul[0] + ")"
kullanıcı_dil_kodu = kullanıcı_dilini_bul[1]
logging.info(_("Kullanıcı dili belirlendi: %s - sistem Karakter kodu: %s"), sistem_dili, kullanıcı_dil_kodu)

# dil dosyaları kontrol: locales klasörü yapısı içersinde hangi dillerin olduğunu bulup aktarma
dil_dosyaları_listesi = os.listdir("locales")  # dil dosyalarının yüklü olduğu klasör
logging.debug(_("Dil dosyaları klasörü kontrolü : %s"), dil_dosyaları_listesi)

# Çeviri dosyalarının tanımlanması ve yüklenmesi
seçilen_dil = ["de"]  # sistem_dili # ilerde belki okuduğu konfirigasyon dosyası içersinden veri alacak.
if seçilen_dil[0] not in dil_dosyaları_listesi:
    logging.warning(_("%s dil klasörleri içinden %s dili bulunamadı."), dil_dosyaları_listesi, seçilen_dil)
    seçilen_dil = öntanımlı_diller  # öntanımlı diller ataması
    logging.info(_("ön tanımlı dil ataması yapıldı. %s"), seçilen_dil)
# çeviri için gerekli olan *.mo dosyası kontrolu. Yok ise bunun için bir mekanizma
dil_varmı = gettext.find("messages", localedir="locales", languages=seçilen_dil)
logging.debug(_("dil dosya kontrolu '%s'"), dil_varmı)
if not dil_varmı:
    logging.warning(_("Gerekli olan \"*.mo\" '%s' dil dosyası bulunamamaktadır."), seçilen_dil)
    dil_varmı = gettext.find("messages", localedir="locales", languages=öntanımlı_diller)
    logging.debug(_("Öntanımlı %s dosyalara bakılıyor."), öntanımlı_diller)
    if not dil_varmı:
        hata_mesajı = _("HATA: Öntanımlı dil {} dosyalarında hata var. Lütfen dil dosyalarını tekrar yükleyin".format(
            öntanımlı_diller))
        print(hata_mesajı)
        logging.warning(hata_mesajı)
        exit()
    else:
        seçilen_dil = öntanımlı_diller
        logging.debug(_("Öntanımlı olan diller yüklendi: %s"), öntanımlı_diller)

try:
    program_dili = gettext.translation("messages", localedir="locales", languages=seçilen_dil)
except:
    hata_mesajı = _("HATA: Dil dosyası için gerekli *.mo dosyası bulunamamıştır. Komuttan çıkılmıştır.")
    logging.warning(hata_mesajı)
    print(hata_mesajı)
    exit()

logging.debug(_("Program dili alınıyor.: %s"), program_dili.info())
program_dili.install()
logging.debug(_("Çeviri yüklendi. (%s)"), seçilen_dil)
argparse._ = program_dili.gettext  # argparse modulundeki çeviriler için _ ye atama yapıldı.
logging.debug(_("Komut sistemi için çeviri yüklendi. (%s)"), seçilen_dil)

# Komut satırı argümanlarının belirlenmesi
argüman_dizesi = argparse.ArgumentParser(description=_("MP4 dosyalarını derlemek için") + sistem_dili)
logging.debug(_("Komut sistemi çalıştırılıyor. Tanımlama yapıldı."))
argüman_dizesi.add_argument(_("girdi"),
                            help=_("Video dosyası girdisi"))
logging.debug(_("Komut sistemine argüman atandı: '%s'"), _("girdi"))
argüman_dizesi.add_argument("-i", "--info",
                            help=_("Video dosyası hakkında bilgi verir."),
                            action="store_true")
logging.debug(_("Komut sistemine argüman atandı: '-i', '--info'"))
argümanlar = argüman_dizesi.parse_args()
logging.debug(_("Komut sistemi argümanlar işlendi."))

# verilen argümanlara göre yapılan işlemler
sonuç = getattr(argümanlar, _("girdi"))  # argümanlar.girdi
logging.debug(_("Burada işlemler yapılıp sonuç çıkacak: sonuç değeri = %s"), sonuç)
if getattr(argümanlar, "info"):  # argümanlar.info:
    logging.debug(_("Argümanlarda -i, --info kullanıldı. Dosya ayrıntıları gelecek."))
    print(_("verilen '{}' dosyası için detaylar:").format(sonuç))
    logging.debug("Dosya ayrıntıları verildi.")
else:
    logging.debug(_("Hiç bir argüman girişi yapılmadı."))
    print(sonuç)
    logging.debug(_("Sonuç verildi: '%s'"), sonuç)
