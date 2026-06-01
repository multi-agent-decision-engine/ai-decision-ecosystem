# Project Memory

Bu dosya, proje bitene kadar rapor ve teslim surecinde ortak hafiza olarak kullanilir. Gecici PR metinleri, teslim plani ve rapor formati notlari kok dizin yerine `docs/internal_notes/` altinda tutulur.

## Son Teknik Durum

- Ana repo: `https://github.com/multi-agent-decision-engine/ai-decision-ecosystem`
- PR #14 merge edildi: LLM agent integration `main` branch'e girdi.
- Local backend Docker container ile calistirildi:
  - Backend: `http://localhost:8000`
  - Frontend: `http://127.0.0.1:5173`
  - DB: PostgreSQL container healthy
- LLM entegrasyonu local Ollama ile test edildi.
  - `MADE_USE_LLM=1`
  - Container icinden host Ollama icin: `LLM_BASE_URL=http://host.docker.internal:11434/v1`
  - API response icinde `rounds[].messages[].metrics.llm` goruldu.
- Frontend build calisti: `npm run build`

## Ekip Gorevleri

- Melike: agent mimarisi, backend API sozlesmesi, detailed simulation response, Docker/API stabilitesi, testler.
- Helin: Agile dataset mapping, normalization, validation, analysis report, calibration hazirligi.
- Afra: React frontend cockpit, backend API entegrasyonu, debate console, executive report UI.

## Rapor Durumu

- Ana taslak: `docs/report/final_report_draft.md`
- Format kaynagi: `docs/report/source/Yazilim_Muhendisligi_Donem_Projesi_Rapor_Formati.docx.pdf`
- Format extract metni: `docs/internal_notes/report_working/rapor_formati_extracted.txt`
- Eksik analiz: `docs/internal_notes/report_working/RAPOR_FORMATI_EKSIK_ANALIZI.md`
- Melike hazir rapor bolumleri:
  - `docs/report/melike_rapor_bolumleri.md`
  - `docs/report/melike_teslim_kontrol.md`

## Rapor Ilerleme Notlari

- Bolum 1 baslatildi: giris, amac/kapsam, hedef kullanicilar, teknoloji tablosu.
- Bolum 4 baslatildi: GitHub repository yapisi, README, branch/PR sureci, code review akisi.
- Jira bolumu simdilik ileri zamana birakildi; once Jira panosu rapora uygun duzenlenecek.
- 2.4 is kurallari ve kisitlamalar bolumu tekrar ele alinacak; `BR-*` kodlari rapor ici Business Rule ID'leridir, Jira ID degildir.

## Root Temizligi Karari

Kok dizindeki gecici dosyalar silinmedi, su klasorlere tasindi:

- `docs/internal_notes/delivery/`
- `docs/internal_notes/pr_notes/`
- `docs/internal_notes/report_working/`
- `docs/internal_notes/data/`
- `docs/report/source/`

Yeni duzenleme karari:

- Roadmap ve proje guncelleme notlari `docs/project/ROADMAP.md` altinda
  ozetlendi; eski uzun dosyalar `docs/project/archive/` altinda saklanacak.
- Veri bilimi notlari `docs/data_science/DATA_SCIENCE_OVERVIEW.md` altinda
  ozetlendi; ayrintili eski dosyalar `docs/data_science/` ve
  `docs/data_science/archive/` altinda tutulacak.
- Kok dizindeki `MEMORY.md` dosyasi proje hafizasina aktarilip
  `docs/internal_notes/legacy/` altina alinacak.
- Kok dizinde rapor gorseli icin sadece ana kullanim dokumanlari birakilacak:
  `README.md`, `README_DATA_SCIENCE.md`, `QUICKSTART.md`.

Bu sayede GitHub repo ana sayfa ekran goruntusu daha temiz gorunur, fakat proje hafizasi kaybolmaz.

## Acik Isler

- Kapak bilgileri doldurulacak: grup no, ogrenci no, soyadlar, ders sorumlusu, Jira linki, teslim tarihi.
- Bolum 2.4 is kurallari resmi metne cevrilecek.
- Bolum 3 Jira/Kanban icin pano duzenlenecek ve ekran goruntuleri alinacak.
- Bolum 5 mimari ve tasarim bolumu temizlenecek.
- Bolum 6 veritabani ve ORM bolumu eklenecek.
- Bolum 7 uygulama gelistirme ve API bolumu eklenecek.
- Bolum 8 test calismalari eklenecek.
- GitHub gorselleri alinacak:
  - repo home
  - branches
  - commit history
  - PR list
  - PR detail/review/checks
