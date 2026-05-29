# Melike — Teslim Kontrol & Kanıt İndeksi

Bu dosya Melike'nin rapor için sorumlu olduğu tüm teslimlerin son durumunu ve dosya yollarını listeler.

## 1. Yazılı Bölümler (Word'e yapıştır)

Tek kaynak: [docs/report/melike_rapor_bolumleri.md](melike_rapor_bolumleri.md)

| Rapor § | Başlık | Durum |
|---|---|---|
| 1.1 | Projenin Amacı ve Kapsamı | ✅ Hazır |
| 2.4 | İş Kuralları ve Kısıtlamalar (BR-01…BR-12) | ✅ Hazır |
| 5.1 | Sistem Mimarisi | ✅ Hazır |
| 5.1.1 | Mimari Diyagram (görsel) | ✅ Hazır |
| 5.1.2 | Katman Sorumlulukları | ✅ Hazır |
| 5.2 | Tasarım Desenleri | ✅ Hazır |
| 6.1 | E-R Modeli | ✅ Hazır |
| 6.2 | İlişkisel Şema | ✅ Hazır |
| 6.3 | ORM Konfigürasyonu ve Entity | ✅ Hazır |
| 6.4 | Tablo İlişkilerinin Modellenmesi | ✅ Hazır |
| 6.5 | Migration Yönetimi | ✅ Hazır |
| 7.2 | API / Servis Katmanı | ✅ Hazır |
| 7.3 | Önemli Kod Parçaları | ✅ Hazır |
| 8.1 | Test Stratejisi | ✅ Hazır |
| 8.2 | Test Senaryoları (UT-01…UT-10) | ✅ Hazır |
| 8.3 | Test Komutu ve Çıktı | ✅ Hazır |

## 2. Görseller (Word'e Resim Olarak Ekle)

| Görsel | Dosya | Boyut |
|---|---|---|
| Mimari Diyagram | `docs/report_assets/diagrams/architecture.png` | ~74 KB PNG (+ SVG yedeği) |
| E-R Diyagramı | `docs/report_assets/diagrams/er_diagram.png` | ~19 KB PNG (+ SVG yedeği) |
| Pytest Sonucu (104 passed) | `docs/report_assets/tests/pytest_output.png` | Terminal stilinde |

## 3. Kod & Veri Kanıtları (Word'e Metin/Kod Bloğu Olarak)

| Kanıt | Dosya | Kullanım Yeri |
|---|---|---|
| `pytest -q` ham metin çıktısı | `docs/report_assets/tests/pytest_output.txt` | §8.3 |
| Canlı `GET /api/v1/scenarios?limit=3` | `docs/report_assets/backend/get_scenarios.json` | §7.2 |
| Canlı `POST /scenarios/5/simulate` | `docs/report_assets/backend/simulate_response.json` | §7.2 |

## 4. Manuel Olarak Toplanacak Ekran Görüntüleri (Sadece Sen Alabilirsin)

### 4.1 GitHub (Melike PR'ları için — §4.3, §4.4)

Kaydedilecek hedef klasör: `docs/report_assets/github/`

| Ekran | Nasıl Alınır | Kayıt Adı |
|---|---|---|
| Repo ana sayfası | github.com/<repo> ana sayfa | `01_repo_home.png` |
| Branches listesi | "branches" sekmesi | `02_branches.png` |
| Commit history | "commits" görünümü | `03_commits.png` |
| PR listesi | Pull requests sekmesi | `04_pr_list.png` |
| PR detay (Melike'nin PR'ı) | PR sayfası, conversation | `05_pr_detail.png` |
| PR review yorumları | Files changed → yorumlar | `06_pr_review_comments.png` |
| PR approve/request changes | Reviewers paneli | `07_pr_review_status.png` |

### 4.2 Jira (§3.2 — Melike Epic'i: "Agent Architecture & Simulation Contract")

Kaydedilecek hedef klasör: `docs/report_assets/jira/`

| Ekran | Kayıt Adı |
|---|---|
| Kanban board (To Do / In Progress / Code Review / Done) | `01_board.png` |
| Melike Epic detayı | `02_epic_melike.png` |
| 2-3 Story/Task kartı detayı | `03_story_1.png`, `04_story_2.png` |
| Bir kartın Development paneli (branch + commit + PR link) | `05_dev_panel.png` |
| Bir kartın Activity/History sekmesi | `06_history.png` |

### 4.3 Diğer (Tüm Ekip Ortak)

- Kapak: grup no, öğrenci no, ad-soyad, repo linki, Jira linki, teslim tarihi.

## 5. Hızlı Tekrar Üretim Komutları

Backend ayakta iken kanıtları yeniden almak için:

```bash
# Test çıktısı
python -m pytest -q --tb=short 2>&1 | tee docs/report_assets/tests/pytest_output.txt
python docs/report_assets/tests/render_pytest_png.py

# Canlı API
curl -s "http://localhost:8000/api/v1/scenarios?limit=3" | python -m json.tool \
  > docs/report_assets/backend/get_scenarios.json
curl -s -X POST http://localhost:8000/api/v1/scenarios/5/simulate | python -m json.tool \
  > docs/report_assets/backend/simulate_response.json

# Diyagramlar (DOT kaynağından)
dot -Tpng docs/report_assets/diagrams/architecture.dot -o docs/report_assets/diagrams/architecture.png
dot -Tpng docs/report_assets/diagrams/er_diagram.dot   -o docs/report_assets/diagrams/er_diagram.png
```

## 6. Son Durum

**Yazılı + görsel + test kanıtı + canlı API kanıtı:** ✅ Hepsi tamamlandı.

**Geriye yalnızca ekran görüntüsü toplama kaldı** — GitHub PR review ekranları ve Jira board/kart ekranları. Bunları yukarıdaki klasör yapısına göre kaydedip Word raporunun "Ekler" bölümüne referans verirsen Melike'nin teslimi %100 kapanır.
