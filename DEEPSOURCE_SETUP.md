# DeepSource Kurulum ve Yapılandırma Rehberi

## Adım 1: DeepSource Hesabı Oluşturma

1. **DeepSource Web Sitesine Gidin:**
   - https://deepsource.io/ adresine gidin
   - "Sign Up" veya "Get Started" butonuna tıklayın

2. **Hesap Oluşturun:**
   - GitHub, GitLab veya Bitbucket hesabınızla kaydolun
   - Email ve şifre ile de kayıt olabilirsiniz

3. **Hesabınıza Giriş Yapın:**
   - Oluşturduğunuz hesaba giriş yapın

---

## Adım 2: API Token Alma

DeepSource API'sini kullanmak için bir token'a ihtiyacınız var:

1. **Settings'e Gidin:**
   - DeepSource dashboard'unda sağ üst köşedeki profil ikonuna tıklayın
   - "Settings" veya "Account Settings" seçeneğine gidin

2. **API Tokens Bölümünü Bulun:**
   - Settings sayfasında "API Tokens" veya "Access Tokens" bölümünü bulun
   - Eğer göremiyorsanız: https://deepsource.io/settings/tokens adresine gidin

3. **Yeni Token Oluşturun:**
   - "Create Token" veya "Generate Token" butonuna tıklayın
   - Token için bir isim verin (örn: "SmartTestAI-Benchmark")
   - Token'ı kopyalayın ve güvenli bir yere kaydedin
   - ⚠️ **ÖNEMLİ:** Token'ı bir daha göremeyeceksiniz, şimdi kaydedin!

---

## Adım 3: Environment Variable Ayarlama

Windows PowerShell'de:

```powershell
# Geçici olarak (sadece bu terminal için)
$env:DEEPSOURCE_API_TOKEN = "your-token-here"

# Kalıcı olarak (sistem genelinde)
[System.Environment]::SetEnvironmentVariable("DEEPSOURCE_API_TOKEN", "your-token-here", "User")
```

Veya Python kodunda direkt kullanabilirsiniz (güvenlik için önerilmez, sadece test için).

---

## Adım 4: DeepSource API Formatını Öğrenme

DeepSource API'sinin çıktı formatını öğrenmek için:

1. **DeepSource API Dokümantasyonunu İnceleyin:**
   - https://deepsource.io/docs/api/ adresine gidin
   - API endpoint'lerini ve response formatlarını inceleyin

2. **Test API Çağrısı Yapın:**
   - Postman veya curl ile test edin
   - Response formatını kontrol edin

---

## Adım 5: Kod Entegrasyonu

`deepsource_runner.py` ve `deepsource_metrics.py` dosyalarını DeepSource'un gerçek API formatına göre güncelleyin.

---

## Alternatif: DeepSource CLI (Eğer Varsa)

Eğer DeepSource'un bir CLI aracı varsa:

1. **CLI'yi Kurun:**
   ```bash
   # Örnek (gerçek komut DeepSource dokümantasyonunda olmalı)
   pip install deepsource-cli
   # veya
   npm install -g deepsource
   ```

2. **CLI'yi Yapılandırın:**
   ```bash
   deepsource auth login
   # Token'ınızı girin
   ```

3. **Test Edin:**
   ```bash
   deepsource analyze /path/to/project --format json
   ```

---

## Sorun Giderme

### Token Bulamıyorum
- DeepSource dashboard'unda Settings > API Tokens bölümüne gidin
- Eğer yoksa, DeepSource'un API desteği olmayabilir (sadece web arayüzü)

### API Çağrısı Çalışmıyor
- Token'ın doğru olduğundan emin olun
- API endpoint URL'sini kontrol edin
- DeepSource dokümantasyonunu inceleyin

### Format Bilinmiyor
- DeepSource web arayüzünden bir analiz çalıştırın
- Network tab'ında API çağrılarını inceleyin
- Response formatını not edin

---

## Sonraki Adımlar

1. DeepSource API formatını öğrendikten sonra `deepsource_metrics.py`'yi güncelleyin
2. `deepsource_runner.py` içindeki API çağrılarını gerçek endpoint'lere göre düzenleyin
3. Test edin ve sonuçları doğrulayın

