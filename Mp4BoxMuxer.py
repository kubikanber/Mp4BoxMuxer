# 1. komut argumanları ve özelikleri yapılacak.
#   Bunun için temel dosya girdisi sonra çıkış verilmez ise aynı yere dönüşmüştürlmüş şekli çıkacak.
#   örnek: Mp4Muxer input.m* kommutu veridiğinde, önce medya dosyası içersinde olanlara bakılacak -info gibi
#       daha sonra benim belşrdeğim öntanımlı şekle göre çıkış dosyası aynı yere sonuna mux elenerek yaratılacak, aynı
#       isimde dosya var ise isminin sonuna sayı eklenecek.
import argparse
import gettext
import locale

# Kullanılan dili belirleme
kullanıcı_dilini_bul = locale.getdefaultlocale()
dili_göster = " (" + kullanıcı_dilini_bul[0] + ")"
kullanıcı_dil_kodu = kullanıcı_dilini_bul[1]

# Çeviri dosyalarının tanımlanması ve yüklenmesi
program_dili = gettext.translation("messages", localedir="locales", languages=["tr", "en"])
program_dili.install()
argparse._ = program_dili.gettext   # argparse modulundeki çeviriler için _ ye atama yapıldı.

# Komut satırı argümanlarının belirlenmesi
argüman_dizesi = argparse.ArgumentParser(description=_("MP4 dosyalarını derlemek için") + dili_göster)
argüman_dizesi.add_argument("girdi",
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
#print(kullanıcı_dilini_bul)