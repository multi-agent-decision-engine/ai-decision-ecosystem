# Quickstart

Bu rehber, projeyi hizlica calistirmak ve rapor icin hangi dosyalara bakilacagini
bulmak icindir.

## Calistirma

Backend ve veritabani icin:

```powershell
docker compose up --build
```

Backend varsayilan adresi:

```text
http://localhost:8000
```

Frontend icin:

```powershell
cd frontend
npm install
npm run dev
```

Frontend varsayilan adresi:

```text
http://127.0.0.1:5173
```

## LLM Modu

Stabil demo icin LLM kapali akisi kullanilabilir.

LLM acik demo icin yerel Ollama calisir durumda olmalidir:

```powershell
$env:MADE_USE_LLM="1"
$env:LLM_BASE_URL="http://host.docker.internal:11434/v1"
```

Kullanilan yerel model ornegi:

```text
qwen2.5:7b
```

## Testler

Backend testleri:

```powershell
pytest
```

Frontend build kontrolu:

```powershell
cd frontend
npm run build
```

## Dokumantasyon Haritasi

Ana proje yol haritasi:

```text
docs/project/ROADMAP.md
```

Veri bilimi ozeti:

```text
docs/data_science/DATA_SCIENCE_OVERVIEW.md
```

Rapor taslagi:

```text
docs/report/final_report_draft.md
```

Teslim ve proje hafizasi:

```text
docs/internal_notes/PROJECT_MEMORY.md
docs/internal_notes/delivery/TESLIM_GOREV_PLANI.md
```

Rapor gorselleri:

```text
docs/report_assets/
```

Eski detay notlari:

```text
docs/project/archive/
docs/data_science/archive/
docs/internal_notes/legacy/
```
