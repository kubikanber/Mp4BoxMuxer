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

# kayıt işlemleri; logging. Basit bir log çıktısı için.
logging.basicConfig(filename="Mp4BoxMuxer.log",
                    filemode="w",
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s: %(message)s")
logging.info("Program başlıyor. Log tanımlamaları yapıldı.")
# log dosyası için kod içersinde gerekli ayarlamalar yapılcak

# Kullanılan dilini belirleme
kullanıcı_dilini_bul = locale.getdefaultlocale()
logging.debug("Yerel dil ve kodu alındı.: %s", kullanıcı_dilini_bul)
dili_göster = " (" + kullanıcı_dilini_bul[0] + ")"
kullanıcı_dil_kodu = kullanıcı_dilini_bul[1]
logging.info("Kullanıcı dili belirlendi: %s - sistem Karakter kodu: %s", dili_göster, kullanıcı_dil_kodu)

# dil dosyaları kontrol: locales klasörü yapısı içersinde hangi dillerin olduğunu bulup aktarma
dil_dosyaları_listesi = os.listdir("locales")  # dil dosyalarının yüklü olduğu klasör
logging.debug("Dil dosyaları klasörü kontrolü : %s", dil_dosyaları_listesi)

# Çeviri dosyalarının tanımlanması ve yüklenmesi
seçilen_dil = ["de"]  # deneme için tanımlanmıştır. Dil dosyaları konrol mekanizması için
if seçilen_dil[0] not in dil_dosyaları_listesi:
    logging.warning("%s dil klasörleri içinden %s dili bulunamadı.", dil_dosyaları_listesi, seçilen_dil)
    seçilen_dil = ["tr"]
    logging.info("ön tanımlı dil ataması yapıldı.")
# çeviri için gerekli olan *.mo dosyası kontrolu. Yok ise bunun için bir mekanizma
dil_varmı = gettext.find("messages", localedir="locales", languages=seçilen_dil)
logging.debug("dil dosya kontrolu %s", dil_varmı)
# TODO : *.mo Dosyası konrool meknizması
program_dili = gettext.translation("messages", localedir="locales", languages=seçilen_dil)
logging.debug("Program dili alınıyor.: %s", program_dili)
program_dili.install()
logging.debug(_("Çeviri yüklendi. (%s)"), seçilen_dil)
argparse._ = program_dili.gettext  # argparse modulundeki çeviriler için _ ye atama yapıldı.
logging.debug(_("Komut sistemi için çeviri yüklendi. (%s)"), seçilen_dil)

# Komut satırı argümanlarının belirlenmesi
argüman_dizesi = argparse.ArgumentParser(description=_("MP4 dosyalarını derlemek için") + dili_göster)
logging.debug(_("Komut sistemi çalıştırılıyor. Tanımlama yapıldı."))
argüman_dizesi.add_argument(_("girdi"),
                            help=_("Video dosyası girdisi"))
logging.debug(_("Komut sistemine arguman atandı: '%s'"), _("girdi"))
argüman_dizesi.add_argument("-i", "--info",
                            help=_("Video dosyası hakkında bilgi verir."),
                            action="store_true")
logging.debug(_("Komut sistemine argüman atandı: '-i', '--info'"))
argümanlar = argüman_dizesi.parse_args()
logging.debug(_("Komut sistemi argümanlar işlendi."))

# verilen argümanlara göre yapılan işlemler
sonuç = getattr(argümanlar, _("girdi"))  # yani birde (argümanlar.girdi) şeklinde değişkene ulaşabiliriz.
logging.debug(_("Burada işlemler yapılıp sonuç çıkacak: sonuç değeri = %s"), sonuç)
if getattr(argümanlar, "info"):  # argümanlar.info:
    logging.debug(_("Argümanlarda -i, --info kullanıldı. Dosya ayrıntıları gelecek."))
    print(_("verilen '{}' dosyası için detaylar:").format(sonuç))  # print gösterimined diğer seçenekler kullanalamalı
    logging.debug("Dosya ayrıntıları verildi.")
else:
    logging.debug(_("Hiç bir argüman girişi yapılmadı."))
    print(sonuç)
    logging.debug(_("Sonuç verildi: '%s'"), sonuç)
