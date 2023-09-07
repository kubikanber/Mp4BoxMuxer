# 1. komut argumanları ve özelikleri yapılacak.
# komut argümanları dil çevirme özellikleri yapıldı.
#       en ve tr loceles klasörü oluşturulup, içersine .po ve mo dosyaları uygun klasör yolları ile konuldu.
# sistem hangi bölgede olduğu alınıp ona göre dil harfı ve kodlaması alındı.


#   Bunun için temel dosya girdisi sonra çıkış verilmez ise aynı yere dönüşmüştürlmüş şekli çıkacak.
#   örnek: Mp4Muxer input.m* kommutu veridiğinde, önce medya dosyası içersinde olanlara bakılacak -info gibi
#       daha sonra benim belşrdeğim öntanımlı şekle göre çıkış dosyası aynı yere sonuna mux elenerek yaratılacak, aynı
#       isimde dosya var ise isminin sonuna sayı eklenecek.

import logging
import argparse
import gettext
import locale
import pdb

# kayıt işlemleri logging. Basit bir log çıktısı için.
logging.basicConfig(filename="Mp4BoxMuxer.log",
                    filemode="w",
                    level=logging.DEBUG,
                    format="%(asctime)s - %(levelname)s: %(message)s")
logging.info("Program başlıyor. Log tanımlamaları yapıldı.")
# log dosyası için kod içersinde gerekli ayarlamalar yapılcak

# Kullanılan dili belirleme
kullanıcı_dilini_bul = locale.getdefaultlocale()
logging.debug("Yerel dil ve kodu alındı.: %s", kullanıcı_dilini_bul)
dili_göster = " (" + kullanıcı_dilini_bul[0] + ")"
kullanıcı_dil_kodu = kullanıcı_dilini_bul[1]
logging.info("Kullanıcı dili belirlendi. %s", dili_göster)

# Çeviri dosyalarının tanımlanması ve yüklenmesi
dil_varmı = gettext.find("messages", localedir="locales", languages=["tr", "en"])
logging.debug("dil dosya kontrolu %s", dil_varmı)
program_dili = gettext.translation("messages", localedir="locales", languages=["de", "en"])
logging.debug("Program dili alınıyor.: %s", program_dili)
program_dili.install()
argparse._ = program_dili.gettext  # argparse modulundeki çeviriler için _ ye atama yapıldı.

# Komut satırı argümanlarının belirlenmesi
argüman_dizesi = argparse.ArgumentParser(description=_("MP4 dosyalarını derlemek için") + dili_göster)
argüman_dizesi.add_argument(_("girdi"),
                            help=_("Video dosyası girdisi"))
argüman_dizesi.add_argument("-i", "--info",
                            help=_("Video dosyası hakkında bilgi verir."),
                            action="store_true")
argümanlar = argüman_dizesi.parse_args()

# verilen argümanlara göre yapılan işlemler
sonuç = argümanlar.girdi
if argümanlar.info:
    print(f"verilen '{argümanlar.girdi}' dosyası için detaylar:")
else:
    print(sonuç)

#### debug kısmı
# print(kullanıcı_dilini_bul)
# type(program_dili)
print(dil_varmı)
