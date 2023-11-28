import yfinance as yf

# Değerlemeyi yapmak istediğiniz şirketin sembolünü belirtin

sembol = "FROTO.IS"

# İstenen getiri oranını tanımlayın
oran = 0.10  # %10 getiri oranını kullanalım

# Gelecekteki yıllık nakit akışlarını tanımlayın (örneğin, 5 yıl boyunca)
gelecekteki_nakit_akislar = [100, 120, 140, 160, 180]  # Her yıl için gelecekteki nakit akışlarını ayarlayın

# İndirimli Nakit Akışı (DCF) analizini hesaplayın
dcf_degeri = 0
for i, nakit_akisi in enumerate(gelecekteki_nakit_akislar):
    dcf_degeri += nakit_akisi / (1 + oran) ** (i + 1)

# Şirket verilerini alın
sirket = yf.Ticker(sembol)
veriler = sirket.history(period="365d")  # Son günlük verileri alabilirsiniz

# Son hisse fiyatını alın
son_fiyat = veriler["Close"].iloc[0]

# Sonuçları yazdırın
print(f"{sembol} Hisse Senedi Değerlemesi (DCF Yöntemi):")
print(f"Son Fiyat: ${son_fiyat:.2f}")
print(f"DCF Değeri: ${dcf_degeri:.2f}")