# DeepSource Entegrasyonu - Adım Adım Rehber

## 🎯 Amaç
DeepSource'u projeye entegre edip, Snyk ile aynı metrik formatında sonuçlar almak.

---

## 📋 ADIM 1: DeepSource Hesabı Oluşturma

### 1.1. DeepSource Web Sitesine Gidin
- Tarayıcınızda https://deepsource.io/ adresine gidin
- "Sign Up" veya "Get Started" butonuna tıklayın

### 1.2. Hesap Oluşturun
- **Seçenek 1:** GitHub hesabınızla giriş yapın (önerilen)
- **Seçenek 2:** Email ve şifre ile kayıt olun

### 1.3. Hesabınıza Giriş Yapın
- Oluşturduğunuz hesaba giriş yapın

---

## 🔑 ADIM 2: API Token Alma

### 2.1. Settings Sayfasına Gidin
- DeepSource dashboard'unda sağ üst köşedeki profil ikonuna tıklayın
- "Settings" veya "Account Settings" seçeneğine gidin
- VEYA direkt şu adrese gidin: https://deepsource.io/settings/tokens

### 2.2. API Tokens Bölümünü Bulun
- Settings sayfasında "API Tokens" veya "Access Tokens" bölümünü bulun
- Eğer göremiyorsanız, DeepSource'un API desteği olmayabilir (sadece web arayüzü)

### 2.3. Yeni Token Oluşturun
- "Create Token" veya "Generate Token" butonuna tıklayın
- Token için bir isim verin: `SmartTestAI-Benchmark`
- Token'ı kopyalayın ve güvenli bir yere kaydedin
- ⚠️ **ÖNEMLİ:** Token'ı bir daha göremeyeceksiniz, şimdi kaydedin!

---

## ⚙️ ADIM 3: Environment Variable Ayarlama

### Windows PowerShell'de:

```powershell
# Geçici olarak (sadece bu terminal için)
$env:DEEPSOURCE_API_TOKEN = "your-token-here"

# Kalıcı olarak (sistem genelinde)
[System.Environment]::SetEnvironmentVariable("DEEPSOURCE_API_TOKEN", "your-token-here", "User")
```

### Kontrol Edin:
```powershell
# Token'ın ayarlandığını kontrol edin
echo $env:DEEPSOURCE_API_TOKEN
```

---

## 🧪 ADIM 4: Test Modu ile Deneme

DeepSource API'sini henüz yapılandırmadıysanız, test modu ile deneyebilirsiniz:

### 4.1. Flask API'yi Başlatın
```powershell
cd backend
python app.py
```

### 4.2. Test Endpoint'ini Çağırın
Yeni bir terminal açın:

```powershell
# Python ile test
python -c "import requests; import json; r = requests.post('http://localhost:5001/scan/deepsource', json={'project': 'flask_demo'}); print(json.dumps(r.json(), indent=2, ensure_ascii=False))"
```

**Beklenen Sonuç:**
- Mock/test verisi dönecek
- Metrikler hesaplanacak
- Sonuç `results/` klasörüne kaydedilecek

---

## 🔍 ADIM 5: DeepSource API Formatını Öğrenme

### 5.1. DeepSource API Dokümantasyonunu İnceleyin
- https://deepsource.io/docs/api/ adresine gidin
- API endpoint'lerini ve response formatlarını inceleyin

### 5.2. DeepSource Web Arayüzünden Test Edin
1. DeepSource dashboard'unda bir repository ekleyin
2. Bir analiz çalıştırın
3. Tarayıcı Developer Tools'u açın (F12)
4. Network tab'ına gidin
5. API çağrılarını inceleyin
6. Response formatını not edin

### 5.3. Örnek API Çağrısı (Postman/curl)
```bash
# Örnek (gerçek endpoint DeepSource dokümantasyonunda olmalı)
curl -X POST https://api.deepsource.io/v1/analyze \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"repository": "your-repo", "format": "json"}'
```

---

## 📝 ADIM 6: Kod Güncelleme

### 6.1. DeepSource API Formatını Öğrendikten Sonra

#### `backend/deepsource_runner.py` dosyasını güncelleyin:
- `run_deepsource_scan()` fonksiyonundaki API endpoint'ini gerçek endpoint'e göre düzenleyin
- Request formatını DeepSource API'sine göre güncelleyin

#### `backend/metrics/deepsource_metrics.py` dosyasını güncelleyin:
- `calculate()` fonksiyonundaki format mapping'i DeepSource'un gerçek formatına göre düzenleyin
- Severity seviyelerini DeepSource'un kullandığı seviyelere göre map edin

### 6.2. Örnek Güncelleme

**DeepSource çıktısı şöyleyse:**
```json
{
  "results": [
    {"severity": "BLOCKER", ...},
    {"severity": "CRITICAL", ...}
  ]
}
```

**`deepsource_metrics.py`'de şöyle güncelleyin:**
```python
issues = raw_data.get("results", [])  # "issues" yerine "results"
severity = issue.get("severity", "").upper()  # Büyük harf

if severity in ["BLOCKER", "CRITICAL"]:
    counts["critical"] += 1
```

---

## ✅ ADIM 7: Test ve Doğrulama

### 7.1. Gerçek DeepSource Taraması Yapın
```powershell
# API'yi başlatın (zaten çalışıyorsa atlayın)
cd backend
python app.py
```

### 7.2. Test Endpoint'ini Çağırın
```powershell
python -c "import requests; import json; r = requests.post('http://localhost:5001/scan/deepsource', json={'project': 'flask_demo'}); print(json.dumps(r.json(), indent=2, ensure_ascii=False))"
```

### 7.3. Sonuçları Kontrol Edin
- Response'da `"success": true` olmalı
- `metrics` objesi Snyk ile aynı formatta olmalı:
  ```json
  {
    "tool_name": "DeepSource",
    "critical": 0,
    "high": 0,
    "medium": 0,
    "low": 0,
    "total_issues": 0,
    "scan_duration": 0.0
  }
  ```

### 7.4. Sonuç Dosyasını Kontrol Edin
```powershell
# results/ klasöründeki en son dosyayı kontrol edin
Get-ChildItem results -Filter "deepsource_*.json" | Sort-Object LastWriteTime -Descending | Select-Object -First 1
```

---

## 🆘 Sorun Giderme

### Token Bulamıyorum
- DeepSource'un API desteği olmayabilir
- DeepSource dashboard'unda Settings > API Tokens bölümünü kontrol edin
- Alternatif: DeepSource CLI kullanmayı deneyin

### API Çağrısı Çalışmıyor
- Token'ın doğru olduğundan emin olun
- API endpoint URL'sini kontrol edin
- DeepSource dokümantasyonunu inceleyin
- Test modu ile devam edin (mock data)

### Format Bilinmiyor
- DeepSource web arayüzünden bir analiz çalıştırın
- Network tab'ında API çağrılarını inceleyin
- Response formatını not edin ve kodu güncelleyin

### Test Modu Çalışmıyor
- Flask API'nin çalıştığından emin olun
- `backend/deepsource_runner.py` dosyasındaki `_get_mock_deepsource_output()` fonksiyonunu kontrol edin

---

## 📚 Sonraki Adımlar

1. ✅ DeepSource hesabı oluşturuldu
2. ✅ API token alındı
3. ✅ Environment variable ayarlandı
4. ⏳ DeepSource API formatı öğrenildi
5. ⏳ Kod güncellendi
6. ⏳ Test edildi ve doğrulandı

---

## 💡 İpuçları

- DeepSource'un API formatını öğrenmek için web arayüzünü kullanın
- Test modu ile önce yapıyı test edin, sonra gerçek API'yi entegre edin
- Snyk ile aynı metrik formatını kullanın (karşılaştırma için)
- Her adımı test edin ve sonuçları kontrol edin

