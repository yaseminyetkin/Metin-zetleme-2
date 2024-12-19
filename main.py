import re
from string import punctuation
import streamlit as st

def durdurma_kelimeleri_dil_sec(dil):
    """
    Belirli bir dildeki durdurma kelimelerini döndüren fonksiyon.
    """
    turkce = set("""
    acaba ama aslında az bazı belki böyle bu çok çünkü da daha de defa diye eğer en fakat gibi hem hiç
    ile ise kez ki kim mi mu mutlaka mı nasıl ne neden o sanki şey siz şu tabii tekrar tüm ve veya ya
    yani yine yok zaman
    """.split())
    ingilizce = set("""
    a an and are as at be but by for if in into is it no not of on or such that the their then there these they this to was will with
    """.split())

    if dil.lower() == "turkce":
        return turkce
    else:
        return ingilizce

def metin_ozetle(metin, ozet_cumle_sayisi=3, kelime_siniri=None, dil="turkce"):
    """
    Metni cümle skorlarına göre özetleyen fonksiyon.
    """
    durdurma_kelimeler = durdurma_kelimeleri_dil_sec(dil)

    # Cümleleri ayır ve temizle
    cumleler = re.split(r'(?<=[.!?])\s+', metin)
    cumleler = [cumle.strip() for cumle in cumleler if cumle.strip()]

    # Kelime frekanslarını hesapla
    kelime_frekanslari = {}
    for cumle in cumleler:
        for kelime in cumle.split():
            kelime = kelime.lower().strip(punctuation)
            if kelime and kelime not in durdurma_kelimeler:
                kelime_frekanslari[kelime] = kelime_frekanslari.get(kelime, 0) + 1

    # Cümle skorlarını hesapla
    cumle_skorlari = []
    for i, cumle in enumerate(cumleler):
        skor = sum(kelime_frekanslari.get(kelime.lower().strip(punctuation), 0)
                   for kelime in cumle.split())
        cumle_skorlari.append((skor, i, cumle))

    # Skora göre sırala
    cumle_skorlari.sort(reverse=True, key=lambda x: x[0])

    # Cümle sayısı ya da kelime sınırına göre özetle
    ozet_cumleler = []
    toplam_kelime = 0
    for skor, i, cumle in sorted(cumle_skorlari, key=lambda x: x[1]):
        if kelime_siniri:
            kelime_sayisi = len(cumle.split())
            if toplam_kelime + kelime_sayisi > kelime_siniri:
                break
            toplam_kelime += kelime_sayisi
        ozet_cumleler.append(cumle)
        if not kelime_siniri and len(ozet_cumleler) == ozet_cumle_sayisi:
            break

    # Özet döndür
    ozet = " ".join(ozet_cumleler)
    return ozet

# Streamlit Arayüzü
st.title("Metin Özetleme Aracı")
st.write("Metni girin, özetlenmiş halini alın!")

# Dil seçimi
dil = st.selectbox("Dil Seçiniz:", ["turkce", "ingilizce"])

# Kullanıcıdan metin girişi
metin = st.text_area("Özetlemek istediğiniz metni girin:")

# Kelime sınırı seçimi
kelime_siniri = st.number_input("Kelime Sınırı:", min_value=1, step=1, value=50)

# Özetleme butonu
if st.button("Metni Özetle"):
    if not metin:
        st.warning("Lütfen bir metin girin!")
    else:
        ozet = metin_ozetle(metin, kelime_siniri=kelime_siniri, dil=dil)
        st.subheader("Özet:")
        st.write(ozet)
