import yfinance as yf
import numpy as np

# Piyasa çarpanları yöntemini kullanarak değerleme yapmak için fonksiyon
def piyasa_carpani_degerlemesi(hisse_kodu, tarih):
  # Fiyat/Kazanç (F/K) çarpanı
  fk_carpani = yf.Ticker(hisse_kodu).info['fcf'] / yf.Ticker(hisse_kodu).info['eps']

  # Piyasa Değeri/Defter Değeri (PD/DD) çarpanı
  pd_dd_carpani = yf.Ticker(hisse_kodu).info['market_cap'] / yf.Ticker(hisse_kodu).info['total_assets']

  # Fiyat/Nakit Akım (F/NA) çarpanı
  fna_carpani = yf.Ticker(hisse_kodu).info['market_cap'] / yf.Ticker(hisse_kodu).info['fcf']

  # Fiyat/Satışlar (F/S) çarpanı
  fs_carpani = yf.Ticker(hisse_kodu).info['market_cap'] / yf.Ticker(hisse_kodu).info['revenue']

  # Piyasa çarpanları ortalaması
  piyasa_carpani_ortalamasi = (fk_carpani + pd_dd_carpani + fna_carpani + fs_carpani) / 4

  return piyasa_carpani_ortalamasi

# Kodu test etmek için örnek
hisse_kodu = 'THYAO.IS'
tarih = '2023-07-07'

piyasa_carpani_ortalamasi = piyasa_carpani_degerlemesi(hisse_kodu, tarih)
print(piyasa_carpani_ortalamasi)