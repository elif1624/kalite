# SmartTestAI - Feature Metrics Engine

Yapay zeka destekli kod analizi test araçlarını (AI Code Analysis Tools) aynı metrikler üzerinden ölçerek karşılaştıran bir benchmark sistemi.

## 🎯 Proje Amacı

"Hangi AI kod analiz aracı daha başarılı?" sorusuna ölçülebilir cevap vermek.

Bu projede şu an **SADECE KOD ANALİZİNE ODAKLANIYORUZ**.

## 🛠️ Desteklenen Araçlar

- ✅ **Snyk Code** - Statik kod analizi (SARIF format desteği)
- ✅ **DeepSource** - AI destekli kod analizi (API entegrasyonu hazır)

## 📁 Proje Yapısı

```
SmartTestAI-feature-metrics-engine/
├── backend/
│   ├── app.py                    # Flask REST API
│   ├── metric_runner.py          # Snyk Code runner
│   ├── deepsource_runner.py      # DeepSource runner
│   ├── metrics/
│   │   ├── base_metric.py        # Abstract metric class
│   │   ├── snyk_metrics.py       # Snyk metric implementation
│   │   ├── deepsource_metrics.py # DeepSource metric implementation
│   │   └── result_model.py       # Standard metric result model
│   └── README.md                 # Backend dokümantasyonu
├── test_projects/                # Test projeleri
│   └── flask_demo/              # Flask test projesi
├── results/                      # Tarama sonuçları (JSON)
└── src/                          # (Gelecek kullanım için)
```

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler

- Python 3.8+
- Snyk CLI (kurulu ve authenticate edilmiş)
- DeepSource API Token (opsiyonel, test modu mevcut)

### 2. API'yi Başlat

```bash
cd backend
python app.py
```

API `http://localhost:5001` adresinde çalışacak.

### 3. Test Senaryoları

**Snyk Code Taraması:**
```bash
curl -X POST http://localhost:5001/scan/code \
  -H "Content-Type: application/json" \
  -d '{"project": "flask_demo"}'
```

**DeepSource Taraması:**
```bash
curl -X POST http://localhost:5001/scan/deepsource \
  -H "Content-Type: application/json" \
  -d '{"project": "flask_demo"}'
```

## 📊 Standart Metrik Formatı

Tüm araçlar aynı metrik formatını kullanır:

```json
{
  "tool_name": "Snyk Code" | "DeepSource",
  "critical": 0,
  "high": 0,
  "medium": 0,
  "low": 0,
  "total_issues": 0,
  "scan_duration": 0.0
}
```

## 🔗 API Endpoint'leri

### Snyk Code
- `POST /scan/code` - Tek proje taraması
- `POST /scan/code/all` - Tüm projeleri tarama

### DeepSource
- `POST /scan/deepsource` - Tek proje taraması
- `POST /scan/deepsource/all` - Tüm projeleri tarama

### Genel
- `GET /projects` - Mevcut projeleri listele

Detaylı API dokümantasyonu için: `backend/API_DOCUMENTATION.md`

## 👥 Ekip Görevleri

### Kişi 1: Snyk Entegrasyonu ✅
- Snyk Code taraması
- SARIF format desteği
- Metrik normalizasyonu

### Kişi 2: DeepSource Entegrasyonu ✅
- DeepSource API entegrasyonu
- Metrik normalizasyonu
- Test modu desteği

### Kişi 3: Otomasyon Script'i (Planlanıyor)
- Otomatik tarama script'i
- Sonuç karşılaştırması

### Kişi 4: Arayüz (Planlanıyor)
- Web arayüzü
- Sonuç görselleştirme

## 📝 Notlar

- Tüm tarama sonuçları `results/` klasörüne kaydedilir
- Dosya formatı: `{tool}_{project}_{timestamp}.json`
- Snyk CLI'nin kurulu ve authenticate edilmiş olması gerekir
- DeepSource için API token gerekli (test modu mevcut)

## 📚 Dokümantasyon

- `backend/README.md` - Backend detaylı dokümantasyonu
- `backend/API_DOCUMENTATION.md` - API endpoint dokümantasyonu
- `backend/DEEPSOURCE_SETUP.md` - DeepSource kurulum rehberi
- `backend/DEEPSOURCE_ADIM_ADIM.md` - DeepSource adım adım rehber

## 🔧 Geliştirme

### Yeni Araç Ekleme

1. `metrics/` klasörüne yeni metric class'ı ekleyin (`BaseMetric`'ten türetin)
2. `backend/` klasörüne yeni runner ekleyin
3. `app.py`'ye yeni endpoint'ler ekleyin
4. Metrikleri standart formata normalize edin

## 📄 Lisans

Bu proje eğitim/araştırma amaçlıdır.
