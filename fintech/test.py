from yahoofinancials import YahooFinancials

# Şirketin sembolünü belirtin
sembol = 'AAPL'

# YahooFinancials nesnesini oluşturun
yf = YahooFinancials(sembol)

# Piyasa Değeri (Market Cap) verisini alın
piyasa_degeri = yf.get_market_cap()

# Toplam Borç (Total Debt) verisini alın
#toplam_borc = yf.get_total_debt()

# Nakit ve Nakit Benzerleri (Cash and Cash Equivalents) verisini alın
nakit_ve_nakit_benzerleri = yf.get_total_cash()

# İşletme Değerini (Enterprise Value) hesaplayın
isletme_degeri = piyasa_degeri + toplam_borc - nakit_ve_nakit_benzerleri

# Sonucu yazdırın
print(f"{sembol} İşletme Değeri (Enterprise Value): ${isletme_degeri:.2f}")
