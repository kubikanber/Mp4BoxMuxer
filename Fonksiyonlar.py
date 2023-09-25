# Mp4BoxMuxer
# Ana kod içersinde tekrarlayan kodlar
# için fonksiyon oluşturulmuştur ve burada tanımlanmıştır.

import gettext
import logging
import platform
import subprocess
import sys
import os

_ = gettext.gettext


# Verilen dosya ismi ve dosya yolunda ilgili .mo dosyasının olup olmadığını konroletmek için
# Dosya var ise dosya yolu ile
# Yok ise None ile dönüş yapar.
# @mo_dosyası: str
# @return
def dil_dosyası_kontrol(mo_dosyası: str, dil_klasör_yolu: str, dil: []):
    dil_varmı = gettext.find(mo_dosyası, localedir=dil_klasör_yolu, languages=dil)
    return dil_varmı


# Gelen komutların çalıştırılması için
def komut_çalıştır(*argüman, **argümanlar):
    logging.debug(_("Komut çalıştır: %s komut çalıştırılacak. argüman değeri %s %s ve argümanlar: %s %s "), argüman,
                  type(argüman), argüman, type(argümanlar), argümanlar)
    komut = komut_argüman_satırı_oluştur(*argüman, **argümanlar)  # TODO:Argüman satırı oluşturma yapılacak.
    komutu_çalıştır(komut)
    print(_("{} komut çalıştırıldı.").format(argüman))
    return


# Çalıştırılaçak komut için argüman satırını oluşturma
def komut_argüman_satırı_oluştur(*argüman, **argümanlar) -> str:
    komut_ekli = ""
    dosya_yolu = ""
    dosya_yolu_ekli = ""
    dosya_ismi = ""
    poz_nolar = []

    logging.debug(_("komut_argüman_satırı_oluştur: Gelen -> argüman %s %s ve argümanlar %s %s"), type(argüman), argüman,
                  type(argümanlar), argümanlar)
    if sözlük_anaftar_kontrol("dosya_yolu", **argümanlar):
        dosya_yolu = str(argümanlar.get("dosya_yolu"))
        dosya_yolu = os.path.normpath(dosya_yolu)
        dosya_yolu_t = os.path.split(dosya_yolu)
        dosya_yolu_s, dosya_ismi = dosya_yolu_t

        for karakter_say in range(len(dosya_yolu)):
            poz_no = dosya_yolu.find("\\", karakter_say, karakter_say + 1)
            if poz_no != -1:
                poz_nolar.append(poz_no)
        logging.debug("komut_argüman_satırı_oluştur: Poz Nolar: %s uzunlluk: %s", poz_nolar, len(poz_nolar))

        dosya_yolu_ekli = dosya_yolu[:int(poz_nolar[0])] + "\\"
        for dizi_say in range(0, len(poz_nolar)):
            birsonraki = 1
            if dizi_say == len(poz_nolar) - 1:
                birsonraki = 0  # liste içersindeki pozisyon
            if int(poz_nolar[dizi_say]) + 1 != int(poz_nolar[dizi_say + birsonraki]):
                dosya_yolu_ekli += dosya_yolu[int(poz_nolar[dizi_say]):int(poz_nolar[dizi_say + birsonraki])] + "\\"
                logging.debug("%s - %s - %s", poz_nolar[dizi_say], dosya_yolu_ekli, poz_nolar[dizi_say + birsonraki])

            else:
                dosya_yolu_ekli += dosya_yolu[int(poz_nolar[dizi_say]):int(poz_nolar[dizi_say])]
                logging.debug("else %s", dosya_yolu_ekli)

        if str(dosya_yolu).startswith("\\"):
            dosya_yolu_ekli = "\\\\" + dosya_yolu_ekli
            logging.debug(_("komut_argüman_satırı_oluştur: ağ yolu saptandı."))
        if str(dosya_ismi).find("'"):
            dosya_ismi = str(dosya_ismi).replace("'", "\\'")
            logging.debug("' bulunudu -> \" ile değişti %s", dosya_ismi)
        logging.debug(_("komut_argüman_satırı_oluştur: dosya_yolu alındı."))
        # TODO: burada argüman içersindeki argümanlar kadar işlem yapması gerekiyor.
    for arüman_say in argüman:
        if arüman_say == "info":
            komut = " -info \"" + dosya_yolu_ekli + dosya_ismi + "\""
            logging.debug(_("komut_argüman_satırı_oluştur: Komut argüman satırı oluşturuldu.\n %s"), komut)
        komut_ekli += komut
        logging.debug(_("komut_argüman_satırı_oluştur: ekli komut : %s"), komut_ekli)
    return komut_ekli


def sözlük_anaftar_kontrol(argüman, **argümanlar) -> bool:
    sonuç = False
    logging.debug(_("Sözlük anahtar kontrol: argümanlar ->type %s ve argüman %s ve %s ve lar= %s"), type(argümanlar),
                  type(argüman), argüman, argümanlar)
    if argüman in argümanlar.keys():
        sonuç = True
        logging.warning(_("%s sözlük içersinde %s anahtarı bulunmamaktadır."), argümanlar, argüman)

    logging.debug(_("Sözlük anahtar kontrol: %s sözlük içersinde %s anahtarı bulunmuştur. değeri = %s"), argümanlar,
                  argüman, argümanlar.get(argüman))
    logging.debug("Sonuç: %s", sonuç)
    return sonuç


def komutu_çalıştır(komut_satırı: str):
    mp4box_komut = "mp4box"
    mp4box_komutu = mp4box_komut + komut_satırı
    logging.debug("komutu_çalıştır: mp4box_komutu = %s", mp4box_komutu)
    if platform.system() == "Windows":
        new_window_command = "cmd.exe  /c start ".split()
        logging.info("komutu_çalıştır: Windows platformu için çalıştırılacak.")
    else:  # XXX this can be made more portable
        new_window_command = "x-terminal-emulator -e".split()
        logging.info("komutu_çalıştır: Başka bir platform için çalıştırılacak.")

    komut = [sys.executable, "-c",
             "import sys,os,subprocess; "
             "print(sys.argv[1]); "
             "dosya = open('temp.txt','w'); "  # video dosyası ismi eklenecek
             "icislem = subprocess.Popen('cmd /u /c " + mp4box_komutu + "', stdout=subprocess.PIPE, stderr=subprocess.STDOUT,text=True,bufsize=1); "
                                                                        "çıktı, hata_ç = icislem.communicate(); "
                                                                        "print('iç çıktı::',çıktı); "
                                                                        "print('iç hata::',hata_ç); "
                                                                        "print('son::',icislem.returncode); "
                                                                        "dosya.write(çıktı); "
                                                                        "dosya.close(); "
                                                                        "input('enter...'); "

             ]
    birleşim = new_window_command + komut + [mp4box_komut]
    logging.debug("komutu_çalıştır: birleşik komut oluşturuldu: %s", birleşim)

    islem = subprocess.Popen(birleşim, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE, text=True,
                             bufsize=1)
    çıktı, hata_ç = islem.communicate()
    logging.debug("komutu_çalıştır: işlem tamamlandı. çıktı: %s - Hata %s ", çıktı, hata_ç)
