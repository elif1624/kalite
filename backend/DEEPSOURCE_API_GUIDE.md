# DeepSource API Kullanım Rehberi

## ⚠️ ÖNEMLİ: DSN vs API Token

**DSN (Data Source Name):** `https://da2d6d49b17d4235bd9d31dd6e072177@app.deepsource.com`
- Bu DSN **hata izleme** için kullanılır (Sentry benzeri)
- API çağrıları için **kullanılmaz**
- API token'a ihtiyacımız var

## 🔍 Network Tab'ında API Çağrılarını Bulma

### Adım 1: Network Tab'ını Filtreleyin

1. **F12** → **Network** tab
2. **Filter** butonlarından **"Fetch/XHR"** seçin
   - Bu, sadece API çağrılarını gösterir
   - JavaScript ve CSS dosyalarını filtreler

### Adım 2: Sayfayı Yenileyin

1. DeepSource dashboard'unda sayfayı yenileyin (F5)
2. Network tab'ında API çağrılarını görün
3. Özellikle şunları arayın:
   - `/api/v1/...` ile başlayan çağrılar
   - `/graphql` çağrıları (DeepSource GraphQL API kullanıyor olabilir)
   - Issue listesi için çağrılar

### Adım 3: API Çağrısını İnceleyin

1. Bir API çağrısına tıklayın
2. **Headers** tab'ına gidin:
   - **Authorization** header'ını kontrol edin
   - Token formatını not edin
3. **Response** tab'ına gidin:
   - JSON formatını inceleyin
   - Issue'ların nasıl yapılandırıldığını görün

## 🔑 API Token Alma

### Yöntem 1: Settings'ten Token Alma

1. DeepSource dashboard → Sağ üst köşe → **Settings**
2. **API Tokens** veya **Access Tokens** bölümünü bulun
3. **Create Token** butonuna tıklayın
4. Token'ı kopyalayın

### Yöntem 2: Network Tab'ından Token Bulma

1. Network tab'ında bir API çağrısına tıklayın
2. **Headers** tab → **Request Headers** bölümüne gidin
3. **Authorization** header'ını bulun
4. Token formatını not edin (genellikle `Bearer TOKEN` veya `Token TOKEN`)

## 📡 DeepSource API Endpoint'leri (Tahmini)

DeepSource genellikle şu endpoint'leri kullanır:

### GraphQL API (Olası)
```
POST https://api.deepsource.io/graphql
```

### REST API (Olası)
```
GET https://api.deepsource.io/v1/repos/{owner}/{repo}/issues
GET https://api.deepsource.io/v1/repos/{owner}/{repo}/analyses
```

### Repository Bilgileri
- Owner: `elif1624`
- Repository: `kalite`

## 🧪 Test API Çağrısı

Network tab'ında gördüğünüz bir API çağrısını kopyalayın:

1. API çağrısına sağ tıklayın
2. **Copy** → **Copy as cURL** seçin
3. Terminal'de çalıştırın
4. Response'u inceleyin

## 📝 Örnek API Çağrısı Formatı

```python
import requests

headers = {
    "Authorization": "Bearer YOUR_TOKEN",  # veya "Token YOUR_TOKEN"
    "Content-Type": "application/json"
}

# Örnek endpoint (gerçek endpoint Network tab'ında görünecek)
response = requests.get(
    "https://api.deepsource.io/v1/repos/elif1624/kalite/issues",
    headers=headers
)

print(response.json())
```

## 🎯 Şimdi Yapılacaklar

1. ✅ Network tab'ını açtınız
2. ⏳ **Fetch/XHR** filtresini seçin
3. ⏳ Sayfayı yenileyin
4. ⏳ API çağrılarını bulun
5. ⏳ Bir API çağrısına tıklayın
6. ⏳ **Headers** ve **Response** tab'larını inceleyin
7. ⏳ Token formatını ve response formatını not edin
8. ⏳ Bana paylaşın, kodu güncelleyeyim

## 💡 İpucu

DeepSource dashboard'unda:
- **Issues** sekmesine gidin
- Network tab'ını açık tutun
- Issues yüklenirken API çağrılarını göreceksiniz
- Bu çağrılar issue listesini getiriyor olmalı

