# DeepSource API Entegrasyonu - Adım Adım Rehber

## ✅ Mevcut Durum
- DeepSource dashboard çalışıyor
- Code Analysis ACTIVE
- 21 aktif issue tespit edildi
- Security issues: 1

## 🎯 Şimdi Yapılacaklar

### ADIM 1: DeepSource API Formatını Öğrenme

#### 1.1. Browser Developer Tools'u Açın
1. DeepSource dashboard'unda **F12** tuşuna basın
2. **Network** tab'ına gidin
3. Sayfayı yenileyin (F5)

#### 1.2. API Çağrılarını İnceleyin
1. Network tab'ında API çağrılarını görün
2. Özellikle şu endpoint'leri arayın:
   - `/api/v1/repos/.../issues` - Issue listesi
   - `/api/v1/repos/.../analyses` - Analiz sonuçları
   - `/api/v1/repos/.../issues/summary` - Özet bilgiler

#### 1.3. Response Formatını Not Edin
1. Bir API çağrısına tıklayın
2. **Response** tab'ına gidin
3. JSON formatını inceleyin
4. Özellikle şunları not edin:
   - Issue'ların nasıl yapılandırıldığı
   - Severity seviyeleri (critical, high, medium, low)
   - Issue sayıları
   - Diğer metrikler

### ADIM 2: DeepSource API Token Alma

#### 2.1. Settings'e Gidin
1. DeepSource dashboard'unda sağ üst köşedeki profil ikonuna tıklayın
2. **Settings** seçeneğine gidin
3. Veya direkt: https://deepsource.io/settings/tokens

#### 2.2. API Token Oluşturun
1. **API Tokens** bölümünü bulun
2. **Create Token** veya **Generate Token** butonuna tıklayın
3. Token için bir isim verin: `SmartTestAI-Benchmark`
4. Token'ı kopyalayın ve güvenli bir yere kaydedin
5. ⚠️ **ÖNEMLİ:** Token'ı bir daha göremeyeceksiniz!

### ADIM 3: Environment Variable Ayarlama

#### Windows PowerShell'de:
```powershell
# Geçici olarak
$env:DEEPSOURCE_API_TOKEN = "your-token-here"

# Kalıcı olarak
[System.Environment]::SetEnvironmentVariable("DEEPSOURCE_API_TOKEN", "your-token-here", "User")
```

#### Kontrol Edin:
```powershell
echo $env:DEEPSOURCE_API_TOKEN
```

### ADIM 4: API Endpoint'ini Bulma

DeepSource API'si genellikle şu formatta çalışır:
- Base URL: `https://api.deepsource.io` veya `https://deepsource.io/api/v1`
- Repository endpoint: `/repos/{owner}/{repo_name}/...`

#### Repository Bilgilerini Bulun:
- Owner: `elif1624`
- Repository: `kalite`

### ADIM 5: Test API Çağrısı

#### Postman veya curl ile test edin:

```bash
# Örnek (gerçek endpoint DeepSource dokümantasyonunda olmalı)
curl -X GET "https://api.deepsource.io/v1/repos/elif1624/kalite/issues" \
  -H "Authorization: Token YOUR_TOKEN" \
  -H "Content-Type: application/json"
```

### ADIM 6: Kod Güncelleme

API formatını öğrendikten sonra:

#### 6.1. `deepsource_runner.py` Güncelleme
- `run_deepsource_scan()` fonksiyonundaki API endpoint'ini gerçek endpoint'e göre düzenleyin
- Request formatını DeepSource API'sine göre güncelleyin

#### 6.2. `deepsource_metrics.py` Güncelleme
- `calculate()` fonksiyonundaki format mapping'i DeepSource'un gerçek formatına göre düzenleyin
- Severity seviyelerini DeepSource'un kullandığı seviyelere göre map edin

### ADIM 7: Test ve Doğrulama

```powershell
# Flask API'yi başlatın
cd backend
python app.py

# Yeni terminal'de test edin
python -c "import requests; import json; r = requests.post('http://localhost:5001/scan/deepsource', json={'project': 'flask_demo'}); print(json.dumps(r.json(), indent=2, ensure_ascii=False))"
```

## 📋 Checklist

- [ ] DeepSource API formatını öğrendim (Network tab'ında inceledim)
- [ ] API token aldım ve environment variable olarak ayarladım
- [ ] API endpoint'ini buldum ve test ettim
- [ ] `deepsource_runner.py` dosyasını güncelledim
- [ ] `deepsource_metrics.py` dosyasını güncelledim
- [ ] Test ettim ve sonuçları doğruladım

## 🆘 Sorun Giderme

### API Token Bulamıyorum
- DeepSource dashboard → Settings → API Tokens
- Eğer yoksa, DeepSource'un API desteği olmayabilir (sadece web arayüzü)

### API Çağrısı Çalışmıyor
- Token'ın doğru olduğundan emin olun
- API endpoint URL'sini kontrol edin
- Repository adını doğru yazdığınızdan emin (owner/repo_name)

### Format Bilinmiyor
- Browser Developer Tools → Network tab'ında API çağrılarını inceleyin
- Response formatını not edin
- DeepSource dokümantasyonunu kontrol edin

## 📚 Kaynaklar

- DeepSource API Dokümantasyonu: https://docs.deepsource.com/docs/api
- DeepSource Dashboard: https://deepsource.io/dashboard

