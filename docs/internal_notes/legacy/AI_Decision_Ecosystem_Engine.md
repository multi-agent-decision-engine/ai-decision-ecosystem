# 🤖 AI Decision Ecosystem Engine
## Multi-Agent Karar Destek Sistemi - Tam Dokümantasyon

---

# 📖 İÇİNDEKİLER

1. [Proje Nedir?](#1-proje-nedir)
2. [Problem ve Çözüm](#2-problem-ve-çözüm)
3. [Sistem Nasıl Çalışır?](#3-sistem-nasıl-çalışır)
4. [Agent'lar Kimdir?](#4-agentlar-kimdir)
5. [Senaryo Sınıflandırma](#5-senaryo-sınıflandırma)
6. [Karar Süreci](#6-karar-süreci)
7. [Gerçek Hayat Örneği](#7-gerçek-hayat-örneği)
8. [Mevcut Durum](#8-mevcut-durum)
9. [Gelecek Planları](#9-gelecek-planları)
10. [Sözlük](#10-sözlük)

---

# 1. PROJE NEDİR?

## 🎯 Tek Cümleyle

> Şirketlerin önemli kararlarını **3 farklı uzman yapay zeka** ile değerlendiren bir karar destek sistemi.

## 📝 Detaylı Açıklama

Bir şirket büyük bir karar vermek istediğinde (örneğin: "25 milyon dolarlık yapay zeka yatırımı yapalım mı?"), genellikle farklı departmanların görüşü alınır:

- **CEO** stratejik açıdan bakar
- **CFO** finansal açıdan bakar  
- **HR** insan kaynakları açısından bakar

Bu proje, bu süreci **otomatikleştiren** bir sistemdir. 3 yapay zeka ajanı, her biri kendi uzmanlık alanından senaryoyu değerlendirir ve ortak bir karar üretir.

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   "25M$ AI yatırımı yapalım mı?"                    │
│                                                     │
│              ┌─────────┐                            │
│              │ SİSTEM  │                            │
│              └────┬────┘                            │
│                   │                                 │
│     ┌─────────────┼─────────────┐                   │
│     ▼             ▼             ▼                   │
│  ┌─────┐      ┌─────┐      ┌─────┐                  │
│  │ CEO │      │ CFO │      │ HR  │                  │
│  │  🎯 │      │  💰 │      │  👥 │                │
│  └──┬──┘      └──┬──┘      └──┬──┘                  │
│     │            │            │                     │
│  Strateji    Finans      İnsan                      │
│   Skoru      Skoru      Kaynağı                     │
│    85          90         50                        │
│     │            │            │                     │
│     └────────────┼────────────┘                     │
│                  ▼                                  │
│           ┌───────────┐                             │
│           │  REVISE   │                             │
│           │ Skor: 71  │                             │
│           └───────────┘                             │
│                                                     │
│   "Ekip eksikliğini giderin, sonra onaylayın"       │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# 2. PROBLEM VE ÇÖZÜM

## ❌ Problem: Tek Bakış Açısı Yetersiz

Geleneksel karar verme süreçlerinde:

| Durum | Sonuç |
|-------|-------|
| Sadece CEO karar verirse | Finansal riskler göz ardı edilebilir |
| Sadece CFO karar verirse | Stratejik fırsatlar kaçırılabilir |
| Sadece HR karar verirse | Büyüme hedefleri aksayabilir |

**Örnek Senaryo:**
> CEO: "Bu yatırım bizi sektör lideri yapar, hemen yapalım!"
> 
> *Ama...*
> - CFO: "Nakit akışımız buna yetmez"
> - HR: "Bu projeyi yapacak ekibimiz yok"

## ✅ Çözüm: Çoklu Perspektif

Sistemimiz **3 farklı bakış açısını** bir araya getirir:

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   GELENEKSEL           BİZİM SİSTEM                 │
│   ────────────         ─────────────                │
│                                                     │
│   CEO ──────► Karar    CEO ────┐                    │
│                                │                    │
│                        CFO ────┼──► Dengeli Karar   │
│                                │                    │
│                        HR  ────┘                    │
│                                                     │
│   Tek perspektif       Çoklu perspektif             │
│   Riskli               Dengeli                      │
│   Hızlı ama hatalı     Kapsamlı                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# 3. SİSTEM NASIL ÇALIŞIR?

## 🔄 Ana Akış

```
ADIM 1                ADIM 2                ADIM 3
───────               ───────               ───────
Senaryo               Sınıflandır           Agent'lara
Girişi                (Tip Belirle)         Gönder
   │                      │                     │
   ▼                      ▼                     ▼
┌─────────┐          ┌─────────┐          ┌─────────┐
│ Bütçe   │          │ Bu bir  │          │ CEO:85  │
│ ROI     │    ──►   │ "team   │    ──►   │ CFO:90  │
│ Risk    │          │ expan-  │          │ HR: 50  │
│ Ekip    │          │ sion"   │          │         │
└─────────┘          └─────────┘          └─────────┘


ADIM 4                ADIM 5
───────               ───────
Ağırlıkları           Final
Uygula                Karar
   │                     │
   ▼                     ▼
┌─────────┐          ┌─────────┐
│ CEO:25% │          │         │
│ CFO:25% │    ──►   │ REVISE  │
│ HR: 50% │          │  (71)   │
│         │          │         │
└─────────┘          └─────────┘
```

## 📋 Adım Adım Açıklama

### ADIM 1: Senaryo Girişi
Kullanıcı 4 temel bilgi girer:

| Alan | Açıklama | Örnek |
|------|----------|-------|
| **Bütçe** | Proje maliyeti (milyon $) | 25 |
| **ROI** | Beklenen getiri (%) | 45 |
| **Risk** | Risk seviyesi (1-10) | 5 |
| **Ekip Hazırlığı** | Mevcut ekip yeterliliği (1-10) | 3 |

### ADIM 2: Sınıflandırma
Sistem, girilen bilgilere bakarak senaryonun **tipini** belirler:

| Senaryo Tipi | Ne Zaman? | Örnek |
|--------------|-----------|-------|
| **high_growth** | Yüksek ROI, düşük risk | "Yeni pazara giriş" |
| **cost_optimization** | Düşük bütçe, tasarruf odaklı | "Süreç iyileştirme" |
| **team_expansion** | Ekip yetersiz | "Yeni departman kurulumu" |
| **strategic_pivot** | Yüksek risk, strateji değişikliği | "İş modeli değişikliği" |
| **maintenance** | Düşük her şey | "Sistem güncellemesi" |

### ADIM 3: Agent Analizi
Her agent kendi perspektifinden değerlendirir:

```
┌─────────────────────────────────────────────────────┐
│ CEO AGENT                                           │
├─────────────────────────────────────────────────────┤
│ Bakış Açısı: Strateji, büyüme, vizyon               │
│                                                     │
│ Değerlendirme:                                      │
│ • ROI yüksek mi?          (+puan)                   │
│ • Stratejik uyum var mı?  (+puan)                   │
│ • Pazar fırsatı var mı?   (+puan)                   │
│                                                     │
│ Çıktı: Skor (0-100) + Gerekçe                       │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ CFO AGENT                                           │
├─────────────────────────────────────────────────────┤
│ Bakış Açısı: Finans, maliyet, nakit akışı           │
│                                                     │
│ Değerlendirme:                                      │
│ • Bütçe makul mü?         (+puan)                   │
│ • ROI yeterli mi?         (+puan)                   │
│ • Finansal risk var mı?   (-puan)                   │
│                                                     │
│ Çıktı: Skor (0-100) + Gerekçe                       │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ HR AGENT                                            │
├─────────────────────────────────────────────────────┤
│ Bakış Açısı: İnsan kaynağı, ekip, kapasite          │
│                                                     │
│ Değerlendirme:                                      │
│ • Ekip yeterli mi?        (+puan)                   │
│ • Yeni işe alım gerekli mi? (-puan)                 │
│ • Eğitim ihtiyacı var mı? (-puan)                   │
│                                                     │
│ Çıktı: Skor (0-100) + Gerekçe                       │
└─────────────────────────────────────────────────────┘
```

### ADIM 4: Ağırlıklı Hesaplama
Senaryo tipine göre hangi agent'ın görüşü daha önemli?

| Senaryo Tipi | CEO | CFO | HR |
|--------------|-----|-----|-----|
| high_growth | **40%** | 35% | 25% |
| cost_optimization | 25% | **50%** | 25% |
| team_expansion | 25% | 25% | **50%** |
| strategic_pivot | **45%** | 30% | 25% |
| maintenance | 33% | 33% | 33% |

**Neden?**
- Ekip sorunu varsa → HR daha önemli
- Tasarruf projesi ise → CFO daha önemli
- Büyüme projesi ise → CEO daha önemli

### ADIM 5: Final Karar

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   Hesaplama:                                        │
│   ──────────                                        │
│   CEO Skoru × CEO Ağırlığı = 85 × 0.25 = 21.25      │
│   CFO Skoru × CFO Ağırlığı = 90 × 0.25 = 22.50      │
│   HR  Skoru × HR  Ağırlığı = 50 × 0.50 = 25.00      │
│                              ─────────────────      │
│                              Final Skor = 68.75     │
│                                                     │
│   Karar Eşikleri:                                   │
│   ───────────────                                   │
│   70+ → APPROVE (Onayla)                            │
│   50-69 → REVISE (Revize Et)                        │
│   <50 → REJECT (Reddet)                             │
│                                                     │
│   ► 68.75 = REVISE                                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# 4. AGENT'LAR KİMDİR?

## 🎯 CEO Agent - Strateji Uzmanı

```
┌─────────────────────────────────────────────────────┐
│                    CEO AGENT                        │
│                       🎯                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│   ROL: Chief Executive Officer (Genel Müdür)        │
│                                                     │
│   ODAK ALANLARI:                                    │
│   • Şirket stratejisi                               │
│   • Büyüme hedefleri                                │
│   • Pazar fırsatları                                │
│   • Rekabet avantajı                                │
│   • Uzun vadeli vizyon                              │
│                                                     │
│   SORU: "Bu proje şirketi ileriye taşır mı?"        │
│                                                     │
│   PUANLAMA KRİTERLERİ:                              │
│   ├── Yüksek ROI (+)                                │
│   ├── Stratejik uyum (+)                            │
│   ├── Pazar potansiyeli (+)                         │
│   └── Rekabet avantajı (+)                          │
│                                                     │
│   ÖRNEK ÇIKTI:                                      │
│   "ROI %45 ile güçlü bir getiri. Stratejik          │
│    hedeflerimizle uyumlu. DESTEK veriyorum."        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 💰 CFO Agent - Finans Uzmanı

```
┌─────────────────────────────────────────────────────┐
│                    CFO AGENT                        │
│                       💰                            |
├─────────────────────────────────────────────────────┤
│                                                     │
│   ROL: Chief Financial Officer (Finans Direktörü)   │
│                                                     │
│   ODAK ALANLARI:                                    │
│   • Bütçe yönetimi                                  │
│   • Maliyet analizi                                 │
│   • Nakit akışı                                     │
│   • Yatırım getirisi                                │
│   • Finansal risk                                   │
│                                                     │
│   SORU: "Bu projenin finansal mantığı var mı?"      │
│                                                     │
│   PUANLAMA KRİTERLERİ:                              │
│   ├── Makul bütçe (+)                               │
│   ├── Yeterli ROI (+)                               │
│   ├── Düşük risk (+)                                │
│   └── Pozitif nakit akışı (+)                       │
│                                                     │
│   ÖRNEK ÇIKTI:                                      │
│   "25M$ yatırım için %45 ROI kabul edilebilir.      │
│    Risk seviyesi orta. FİNANSAL OLARAK UYGUN."      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 👥 HR Agent - İnsan Kaynakları Uzmanı

```
┌─────────────────────────────────────────────────────┐
│                    HR AGENT                         │
│                       👥                           │
├─────────────────────────────────────────────────────┤
│                                                     │
│   ROL: Human Resources (İnsan Kaynakları)           │
│                                                     │
│   ODAK ALANLARI:                                    │
│   • Ekip kapasitesi                                 │
│   • Yetenek ihtiyacı                                │
│   • İşe alım gereksinimleri                         │
│   • Eğitim ihtiyaçları                              │
│   • Organizasyonel etki                             │
│                                                     │
│   SORU: "Bu projeyi yapacak ekibimiz var mı?"       │
│                                                     │
│   PUANLAMA KRİTERLERİ:                              │
│   ├── Yeterli ekip (+)                              │
│   ├── Mevcut yetkinlikler (+)                       │
│   ├── Az işe alım ihtiyacı (+)                      │
│   └── Düşük eğitim ihtiyacı (+)                     │
│                                                     │
│   ÖRNEK ÇIKTI:                                      │
│   "Ekip hazırlığı 3/10. Bu proje için en az 8       │
│    yeni çalışan gerekli. NÖTR - Önce işe alım."      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🔄 Agent'lar Arası İletişim

```
┌─────────────────────────────────────────────────────┐
│                    ROUND 1                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│   CEO: "ROI yüksek, stratejik uyum var" → 85        │
│   CFO: "Finansal olarak makul"          → 90        │
│   HR:  "Ekip yetersiz, işe alım gerek"  → 50        │
│                                                     │
├─────────────────────────────────────────────────────┤
│                    ROUND 2                          │
├─────────────────────────────────────────────────────┤
│                                                     │
│   CEO görüyor: CFO olumlu, HR olumsuz               │
│   CFO görüyor: CEO olumlu, HR olumsuz               │
│   HR görüyor:  CEO ve CFO olumlu                    │
│                                                     │
│   (Şu an: Görüyorlar ama tepki vermiyorlar)         │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# 5. SENARYO SINIFLANDIRMA

## 🏷️ 5 Senaryo Tipi

Sistem, her senaryoyu otomatik olarak 5 tipten birine sınıflandırır:

### 1️⃣ HIGH_GROWTH (Yüksek Büyüme)

```
┌─────────────────────────────────────────────────────┐
│ HIGH_GROWTH                                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ÖZELLİKLER:                                         │
│ • Yüksek ROI (>%30)                                 │
│ • Düşük-Orta risk (<6)                              │
│ • Büyüme odaklı                                     │
│                                                     │
│ ÖRNEK: Yeni pazara giriş, ürün lansmanı             │
│                                                     │
│ AĞIRLIKLAR:                                         │
│ ├── CEO: %40 (stratejik vizyon önemli)              │
│ ├── CFO: %35                                        │
│ └── HR:  %25                                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 2️⃣ COST_OPTIMIZATION (Maliyet Optimizasyonu)

```
┌─────────────────────────────────────────────────────┐
│ COST_OPTIMIZATION                                   │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ÖZELLİKLER:                                         │
│ • Düşük bütçe (<$10M)                               │
│ • Düşük risk (<4)                                   │
│ • Tasarruf odaklı                                   │
│                                                     │
│ ÖRNEK: Süreç iyileştirme, otomasyon                 │
│                                                     │
│ AĞIRLIKLAR:                                         │
│ ├── CEO: %25                                        │
│ ├── CFO: %50 (finansal analiz kritik)               │
│ └── HR:  %25                                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 3️⃣ TEAM_EXPANSION (Ekip Genişletme)

```
┌─────────────────────────────────────────────────────┐
│ TEAM_EXPANSION                                      │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ÖZELLİKLER:                                         │
│ • Düşük ekip hazırlığı (<5)                         │
│ • İşe alım ihtiyacı var                             │
│                                                     │
│ ÖRNEK: Yeni departman kurulumu, büyük proje         │
│                                                     │
│ AĞIRLIKLAR:                                         │
│ ├── CEO: %25                                        │
│ ├── CFO: %25                                        │
│ └── HR:  %50 (insan kaynağı kritik)                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 4️⃣ STRATEGIC_PIVOT (Stratejik Dönüşüm)

```
┌─────────────────────────────────────────────────────┐
│ STRATEGIC_PIVOT                                     │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ÖZELLİKLER:                                         │
│ • Yüksek risk (>7)                                  │
│ • Yüksek bütçe (>$20M)                              │
│ • Strateji değişikliği                              │
│                                                     │
│ ÖRNEK: İş modeli değişikliği, satın alma            │
│                                                     │
│ AĞIRLIKLAR:                                         │
│ ├── CEO: %45 (stratejik karar kritik)               │
│ ├── CFO: %30                                        │
│ └── HR:  %25                                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### 5️⃣ MAINTENANCE (Bakım/Rutin)

```
┌─────────────────────────────────────────────────────┐
│ MAINTENANCE                                         │
├─────────────────────────────────────────────────────┤
│                                                     │
│ ÖZELLİKLER:                                         │
│ • Düşük bütçe                                       │
│ • Düşük risk                                        │
│ • Düşük ROI                                         │
│ • Rutin işlemler                                    │
│                                                     │
│ ÖRNEK: Sistem güncellemesi, altyapı bakımı          │
│                                                     │
│ AĞIRLIKLAR:                                         │
│ ├── CEO: %33 (eşit dağılım)                         │
│ ├── CFO: %33                                        │
│ └── HR:  %33                                        │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🔄 Sınıflandırma Nasıl Yapılıyor?

**Şu anki yöntem: KURAL TABANLI**

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   GİRİŞ: budget=25, roi=45, risk=5, team=3          │
│                                                     │
│   KURALLAR:                                         │
│   ─────────                                         │
│                                                     │
│   1. team <= 4?                                     │
│      ├── EVET → team_expansion                      │
│      └── HAYIR → devam                              │
│                                                     │
│   2. roi >= 30 AND risk <= 5?                       │
│      ├── EVET → high_growth                         │
│      └── HAYIR → devam                              │
│                                                     │
│   3. budget < 10 AND risk <= 3?                     │
│      ├── EVET → cost_optimization                   │
│      └── HAYIR → devam                              │
│                                                     │
│   4. risk >= 7 AND budget > 20?                     │
│      ├── EVET → strategic_pivot                     │
│      └── HAYIR → devam                              │
│                                                     │
│   5. Hiçbiri değilse → maintenance                  │
│                                                     │
│   ÇIKTI: team_expansion (team=3 düşük)              │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# 6. KARAR SÜRECİ

## 📊 Karar Eşikleri

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   0        25        50        70       100         │
│   │─────────│─────────│─────────│─────────│         │
│   │  REJECT │  REJECT │  REVISE │ APPROVE │         │
│   │   ❌    │    ❌   │   ⚠️    │   ✅    │       │
│                                                     │
│   REJECT (0-49): Projeyi reddet                     │
│   REVISE (50-69): Revizyonla tekrar değerlendir     │
│   APPROVE (70-100): Projeyi onayla                  │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🧮 Hesaplama Örneği

```
┌─────────────────────────────────────────────────────┐
│ SENARYO: AI Platform Yatırımı                       │
├─────────────────────────────────────────────────────┤
│                                                     │
│ GİRİŞ:                                              │
│ • Bütçe: $25M                                       │
│ • ROI: %45                                          │
│ • Risk: 5/10                                        │
│ • Ekip Hazırlığı: 3/10                              │
│                                                     │
├─────────────────────────────────────────────────────┤
│ SINIFLANDIRMA:                                      │
│ • Tip: team_expansion                               │
│ • Sebep: Ekip hazırlığı düşük (3/10)                │
│                                                     │
├─────────────────────────────────────────────────────┤
│ AGENT SKORLARI:                                     │
│ • CEO: 85 (Strateji uygun)                          │
│ • CFO: 90 (Finans olumlu)                           │
│ • HR:  50 (Ekip yetersiz)                           │
│                                                     │
├─────────────────────────────────────────────────────┤
│ AĞIRLIKLAR (team_expansion için):                   │
│ • CEO: %25                                          │
│ • CFO: %25                                          │
│ • HR:  %50                                          │
│                                                     │
├─────────────────────────────────────────────────────┤
│ HESAPLAMA:                                          │
│                                                     │
│   (85 × 0.25) + (90 × 0.25) + (50 × 0.50)           │
│ = 21.25 + 22.50 + 25.00                             │
│ = 68.75                                             │
│                                                     │
├─────────────────────────────────────────────────────┤
│ KARAR: REVISE (68.75 < 70)                          │
│                                                     │
│ ANLAMI: "Projeyi onaylamadan önce ekip              │
│          eksikliğini giderin."                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

## 🔄 Normal vs Akıllı Hesaplama

``` 
┌─────────────────────────────────────────────────────┐
│ NORMAL ORTALAMA (Sınıflandırma olmadan)             │
├─────────────────────────────────────────────────────┤
│                                                     │
│   (85 + 90 + 50) / 3 = 75                           │
│   Karar: APPROVE ✅                                │
│                                                     │
│   SORUN: Ekip yetersizliği göz ardı edildi!         │
│                                                     │
├─────────────────────────────────────────────────────┤
│ AKILLI ORTALAMA (Sınıflandırma ile)                 │
├─────────────────────────────────────────────────────┤
│                                                     │
│   (85 × 0.25) + (90 × 0.25) + (50 × 0.50) = 68.75   │
│   Karar: REVISE ⚠️                                  │
│                                                     │
│   FAYDA: Ekip sorunu tespit edildi!                 │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# 7. GERÇEK HAYAT ÖRNEĞİ

## 📖 Senaryo: E-Ticaret Şirketi AI Yatırımı

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   ŞİRKET: TechMart E-Ticaret                        │
│   KARAR: Yapay zeka tabanlı öneri sistemi           │
│          yatırımı yapılsın mı?                      │
│                                                     │
│   PROJE BİLGİLERİ:                                  │
│   • Bütçe: $15 milyon                               │
│   • Beklenen ROI: %60                               │
│   • Risk Seviyesi: 4/10                             │
│   • Mevcut Ekip Hazırlığı: 8/10                     │
│                                                     │
└─────────────────────────────────────────────────────┘
```

### Adım 1: Sınıflandırma

```
Sistem: "ROI %60 (>%30), Risk 4 (<=5)"
     → Tip: HIGH_GROWTH
     → CEO görüşü daha önemli (%40)
```

### Adım 2: Agent Analizleri

```
┌─────────────────────────────────────────────────────┐
│ CEO AGENT                                           │
├─────────────────────────────────────────────────────┤
│ "E-ticarette AI öneri sistemleri artık standart.    │
│  Rakiplerimiz zaten kullanıyor. %60 ROI ile         │
│  yatırımın geri dönüşü 2 yılda mümkün.              │
│  Stratejik olarak DESTEKLIYORUM."                   │
│                                                     │
│ SKOR: 92/100                                        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ CFO AGENT                                           │
├─────────────────────────────────────────────────────┤
│ "$15M yatırım için %60 ROI oldukça iyi.             │
│  Risk seviyesi kabul edilebilir.                    │
│  Nakit akışımız bu yatırımı kaldırır.               │
│  Finansal olarak UYGUN."                            │
│                                                     │
│ SKOR: 88/100                                        │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ HR AGENT                                            │
├─────────────────────────────────────────────────────┤
│ "Ekip hazırlığı 8/10 - mevcut veri bilimi           │
│  ekibimiz projeyi yürütebilir.                      │
│  Sadece 2 ek mühendis yeterli.                      │
│  İnsan kaynağı açısından UYGUN."                    │
│                                                     │
│ SKOR: 85/100                                        │
└─────────────────────────────────────────────────────┘
```

### Adım 3: Ağırlıklı Hesaplama

```
Ağırlıklar (high_growth): CEO=%40, CFO=%35, HR=%25

Hesaplama:
(92 × 0.40) + (88 × 0.35) + (85 × 0.25)
= 36.8 + 30.8 + 21.25
= 88.85
```

### Adım 4: Final Karar

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   FINAL SKOR: 88.85                                 │
│                                                     │
│   KARAR: ✅ APPROVE (ONAYLA)                        │
│                                                     │
│   ÖZET:                                             │
│   • CEO: Stratejik uyum mükemmel                    │
│   • CFO: Finansal olarak sağlam                     │
│   • HR: Ekip hazır                                  │
│                                                     │
│   ÖNERİ: "Proje onaylanabilir. 2 ek mühendis        │
│          işe alımı yapılmalı."                      │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# 8. MEVCUT DURUM

## ✅ Tamamlanan Özellikler

| # | Özellik | Açıklama |
|---|---------|----------|
| 1 | Multi-Agent Sistemi | CEO, CFO, HR agentları |
| 2 | Round-Based Tartışma | Agentlar önceki mesajları görüyor |
| 3 | Konsensüs Algılama | Erken sonlandırma |
| 4 | Senaryo Sınıflandırma | 5 tip (kural tabanlı) |
| 5 | Dinamik Ağırlıklar | Tipe göre otomatik |
| 6 | REST API | 8 endpoint |
| 7 | Veritabanı | 105+ senaryo |
| 8 | Dashboard | HTML arayüz |
| 9 | Testler | 86 test geçiyor |
| 10 | Container | Docker deployment |

## ⚠️ Mevcut Kısıtlamalar

### 1. Sınıflandırma Kural Tabanlı

```
MEVCUT:
if team_readiness <= 4:
    return "team_expansion"

OLMASİ GEREKEN:
model.predict([budget, roi, risk, team])  # ML tabanlı
```

### 2. Agentlar Tepki Vermiyor

```
MEVCUT:
CEO görüyor: "HR skoru 50"
CEO tepkisi: (yok, aynı skoru veriyor)

OLMASİ GEREKEN:
CEO görüyor: "HR skoru 50"
CEO tepkisi: "HR'ın endişelerini dikkate alarak
              skorumu 85'ten 75'e düşürüyorum"
```

### 3. Veri Öğrenimde Kullanılmıyor

```
MEVCUT:
105 senaryo → Sadece depolanıyor

OLMASİ GEREKEN:
105 senaryo → Eğitim verisi olarak kullanılıyor
```

## 📊 Gerçek Hayata Yakınlık

```
┌─────────────────────────────────────────────────────┐
│                                                     │
│   MEVCUT SEVİYE                                     │
│   ──────────────────────────────────────            │
│   [████████████████████░░░░░░░░░░] %70-75           │
│                                                     │
│   ✅ Mimari: Üretim seviyesi                        │
│   ✅ API: Üretim seviyesi                           │
│   ✅ Database: Üretim seviyesi                      │
│   ⚠️ ML: Kural tabanlı (geliştirilmeli)             │
│   ⚠️ Agent: Statik (reaktif olmalı)                 │
│   ❌ LLM: Mock (gerçek entegrasyon yok)             │
│                                                     │
└─────────────────────────────────────────────────────┘
```

---

# 9. GELECEK PLANLARI

## 🗺️ Yol Haritası

```
┌─────────────────────────────────────────────────────┐
│ FAZ 8: Gerçek ML Sınıflandırma                      │
├─────────────────────────────────────────────────────┤
│ • scikit-learn ile model eğitimi                    │
│ • 105 veri ile train/test                           │
│ • /api/v1/ml/train endpoint'i                       │
│ • Model kaydetme/yükleme                            │
│ • Tahmini süre: 1-2 saat                            │
└─────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│ FAZ 9: Reaktif Agentlar                             │
├─────────────────────────────────────────────────────┤
│ • Agentlar birbirinin skoruna tepki versin          │
│ • Uzlaşma/ikna mekanizması                          │
│ • Görüş değişikliği takibi                          │
│ • Tahmini süre: 2-3 saat                            │
└─────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│ FAZ 10: Feedback Loop                               │
├─────────────────────────────────────────────────────┤
│ • Karar sonuçlarını kaydet                          │
│ • Model performansını ölç                           │
│ • Otomatik yeniden eğitim                           │
│ • Tahmini süre: 1-2 saat                            │
└─────────────────────────────────────────────────────┘
           │
           ▼
┌─────────────────────────────────────────────────────┐
│ FAZ 11: LLM Entegrasyonu (Opsiyonel)                │
├─────────────────────────────────────────────────────┤
│ • OpenAI/Ollama API bağlantısı                      │
│ • Doğal dilde gerekçeler                            │
│ • Dinamik tartışma                                  │
│ • Tahmini süre: 3-4 saat                            │
└─────────────────────────────────────────────────────┘
```

---

# 10. SÖZLÜK

| Terim | Açıklama |
|-------|----------|
| **Agent** | Belirli bir rolde (CEO, CFO, HR) çalışan yapay zeka modülü |
| **Orkestratör** | Agent'ları koordine eden ve final kararı üreten sistem |
| **Senaryo** | Değerlendirilecek iş kararı (yatırım, proje vb.) |
| **Sınıflandırma** | Senaryonun tipini belirleme işlemi |
| **Ağırlık** | Her agent'ın karardaki etkisini belirleyen yüzde |
| **ROI** | Return on Investment - Yatırım getirisi |
| **Round** | Agent'ların görüş bildirdiği tur |
| **Konsensüs** | Tüm agent'ların benzer görüşte olması |
| **Agregasyon** | Skorların birleştirilmesi |
| **APPROVE** | Projenin onaylanması kararı |
| **REVISE** | Projenin revizyona gönderilmesi kararı |
| **REJECT** | Projenin reddedilmesi kararı |
| **ML** | Machine Learning - Makine Öğrenimi |
| **LLM** | Large Language Model - Büyük Dil Modeli |
| **Kural Tabanlı** | Sabit IF/ELSE kurallarıyla çalışan sistem |
| **Reaktif** | Diğer agent'ların görüşlerine tepki veren |

---

# 📎 EK: HIZLI BAŞVURU

## Sistem Başlatma

```
1. Docker'ı başlat
2. http://localhost:8000/docs - API test
3. static/index.html - Dashboard
```

## Senaryo Oluşturma

```
POST /api/v1/scenarios
{
  "name": "Proje Adı",
  "budget_million_usd": 25.0,
  "expected_roi_percent": 45.0,
  "risk_level": 5,
  "team_readiness": 7
}
```

## Simülasyon Çalıştırma

```
POST /api/v1/scenarios/{id}/simulate
```

## Sonuç Görüntüleme

```
GET /api/v1/scenarios/{id}/simulation
```

---

*Dokümantasyon Tarihi: 4 Mart 2026*
*Versiyon: 1.0*