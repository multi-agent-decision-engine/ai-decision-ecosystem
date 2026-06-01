# Project Roadmap

Bu dosya, kok dizinde daginik duran proje dokumantasyonunu tek bir okunabilir
ozette toplamak icin hazirlandi. Eski ayrintili notlar `docs/project/archive/`
altinda saklanir; rapor ve GitHub goruntuleri icin bu dosya ana kaynak olarak
kullanilabilir.

## Proje Ozeti

Multi-Agent Decision Engine, sirket kararlarini CEO, CFO ve HR bakis acilarindan
analiz eden bir karar destek sistemidir. Sistem; senaryo metnini ve sayisal
parametreleri alir, ajan bazli skorlar uretir, karari `APPROVE`, `REVISE` veya
`REJECT` olarak siniflandirir ve karar gerekcelerini API uzerinden dondurur.

PR #14 sonrasi sistemde LLM destekli aciklama katmani da vardir. Demo veya
stabil test akisi icin LLM kapali calistirilabilir; yerel Ollama hazirsa
`MADE_USE_LLM=1` ile aciklama uretimi aktif edilir.

## Tamamlanan Ana Basliklar

- FastAPI tabanli backend servisleri kuruldu.
- PostgreSQL ve Docker Compose ile calisma ortami hazirlandi.
- CEO, CFO ve HR agent mantigi uygulandi.
- Senaryo siniflandirma ve karar esigi kurallari eklendi.
- React frontend ilk cockpit arayuzu gelistirildi.
- Backend ile frontend arasinda temel API baglantisi test edildi.
- Local Ollama uzerinden LLM entegrasyonu denendi.
- Pytest ve frontend build kontrolleri calistirildi.
- GitHub PR, issue ve branch akisi rapora uygun hale getirilmeye baslandi.

## Teknik Yol Haritasi

### Faz 1 - Cekirdek Karar Motoru

Durum: Tamamlandi.

- Senaryo girdisi alinir.
- Ajanlar kendi skorlarini uretir.
- Sistem toplam skora gore nihai karar verir.
- API yaniti frontend ve rapor icin okunabilir formatta dondurulur.

### Faz 2 - Veri Bilimi Katmani

Durum: Buyuk olcude tamamlandi, rapor icin duzenleniyor.

- Gercek veri setleri incelendi.
- Agile proje verileri karar senaryolarina map edildi.
- Sentetik veri ve model egitimi stratejisi belirlendi.
- Agent skorlarini daha tutarli hale getirmek icin kalibrasyon plani yazildi.

### Faz 3 - LLM Entegrasyonu

Durum: Calisir durumda, demo kalitesi ayrica iyilestirilebilir.

- LLM kapali mod varsayilan ve stabil akistir.
- LLM acik mod yerel Ollama ile calisir.
- Backend yanitinda `metrics.llm=True` ile LLM kullanimi izlenebilir.
- Prompt kalitesi, Turkce karakterler ve daha tutarli gerekce uretimi sonraki
  iyilestirme basliklari olarak durur.

### Faz 4 - Frontend Demo Akisi

Durum: Temel baglanti mevcut, UI akisi icin kalan isler issue olarak acildi.

- Senaryo girisi ve API sonucunun gosterimi hazirlandi.
- Debate console, executive report ve browser demo gecisi Afra tarafinda
  tamamlanacak isler olarak ayrildi.

### Faz 5 - Rapor ve Teslim

Durum: Devam ediyor.

- Rapor formati PDF olarak `docs/report/source/` altinda tutuluyor.
- Taslak rapor `docs/report/final_report_draft.md` uzerinden ilerliyor.
- Jira, GitHub, test, mimari ve veritabani gorselleri rapora eklenecek.

## Rapor Icin Kullanilacak Kaynaklar

- Ana rapor taslagi: `docs/report/final_report_draft.md`
- Proje hafizasi: `docs/internal_notes/PROJECT_MEMORY.md`
- Veri bilimi ozeti: `docs/data_science/DATA_SCIENCE_OVERVIEW.md`
- Teslim plani: `docs/internal_notes/delivery/TESLIM_GOREV_PLANI.md`
- Rapor gorselleri: `docs/report_assets/`

## Guncel Riskler

- Jira panosu rapor gorseline uygun sekilde sonradan duzenlenecek.
- LLM acik mod yerel modele bagimli oldugu icin demo oncesi yeniden smoke test
  edilmelidir.
- Frontend demo akisinda Afra'ya acilan islerin kapanma durumu takip edilmelidir.
- Kok dizinde sadece kullaniciya acik dokumanlar kalmali; calisma notlari
  `docs/internal_notes/` altinda tutulmalidir.
