# BMÜ326 Yazılım Mühendisliği Dönem Projesi Raporu

## Kapak Bilgileri

**Proje Adı:** AI Decision Ecosystem Engine / Multi-Agent Decision Engine

**Grup No:** [Grup numarası eklenecek]

**Takım Üyeleri:**

| Öğrenci No | Ad Soyad | Temel Sorumluluk |
|---|---|---|
| [Öğrenci No] | Melike [Soyad] | Agent mimarisi, backend API sözleşmesi, Docker/API stabilitesi |
| [Öğrenci No] | Helin [Soyad] | Veri bilimi, dataset normalization, validation ve analiz raporu |
| [Öğrenci No] | Afra [Soyad] | Frontend cockpit, backend API entegrasyonu, debate console ve rapor UI |

**Ders Sorumlusu:** [Öğretim üyesinin adı eklenecek]

**GitHub Repo Linki:** https://github.com/multi-agent-decision-engine/ai-decision-ecosystem

**Jira Proje Linki:** [Jira proje linki eklenecek]

**Teslim Tarihi:** [GG/AA/YYYY]

---

# 1. Giriş ve Proje Tanımı

## 1.1 Projenin Amacı ve Kapsamı

AI Decision Ecosystem Engine, iş kararlarını yalnızca tek bir skorla değil, farklı uzman bakış açılarını birlikte değerlendirerek yorumlayan bir karar destek sistemidir. Projede karar sürecini temsil etmek için üç temel ajan kullanılmıştır: CEO, CFO ve HR. Bu ajanlar aynı iş senaryosunu kendi uzmanlık alanlarına göre inceler; CEO stratejik büyüme ve pazar etkisine, CFO finansal risk ve getiri dengesine, HR ise ekip hazırlığı ve operasyonel kapasiteye odaklanır.

Sistemin temel amacı, bir yatırım ya da proje senaryosu için daha açıklanabilir bir karar süreci oluşturmaktır. Kullanıcı sisteme senaryonun adı, açıklaması, bütçesi, beklenen ROI oranı, risk seviyesi ve takım hazırlık düzeyi gibi bilgileri girer. Backend bu girdileri standart bir senaryo modeli olarak işler. Daha sonra ajanlar senaryoyu birden fazla turda değerlendirir. İlk turda her ajan kendi bağımsız analizini üretir; sonraki turda ise önceki ajan mesajları dikkate alınır. Bu yapı sayesinde karar çıktısı sadece "APPROVE", "REVISE" veya "REJECT" gibi bir sonuçtan ibaret kalmaz; kararın hangi gerekçelerle oluştuğu da görülebilir.

Proje kapsamında geliştirilen sistem üç ana parçadan oluşur. İlk parça FastAPI tabanlı backend servisidir. Backend senaryo oluşturma, senaryo listeleme, simülasyon çalıştırma, ajan mesajlarını üretme, senaryo sınıflandırma ve final karar hesaplama sorumluluklarını taşır. İkinci parça React ve Vite ile geliştirilen frontend cockpit arayüzüdür. Bu arayüz, senaryo listesini backend'den alır, simülasyonu başlatır, ajan çıktıları ile tartışma mesajlarını gösterir ve executive report bölümünü oluşturur. Üçüncü parça ise veri bilimi tarafıdır. Agile proje verisi normalize edilmiş, doğrulama kontrollerinden geçirilmiş ve ileride ajan kalibrasyonu için kullanılabilecek bir formata dönüştürülmüştür.

Sistemde karar üretimi deterministik kurallara dayanmaktadır. Ajanların stance, confidence ve metrik alanları backend domain kuralları ile hesaplanır. Proje sonunda LLM destekli gerekçe zenginleştirme katmanı eklenmiştir. Bu katmanda yerel Ollama modeli, ajanların `reasoning` metnini daha doğal ve bağlamsal hâle getirmek için kullanılabilir. Ancak LLM çıktısı nihai kararı doğrudan değiştirmez. LLM erişilemezse veya ürettiği metin deterministik stance ile çelişirse sistem otomatik olarak temel ajan gerekçesine geri döner. Bu tercih, demo sırasında sistemin kararlı çalışmasını ve karar mantığının kontrol altında kalmasını sağlar.

Projenin kapsamına giren başlıca işler şunlardır:

- CEO, CFO ve HR ajanlarından oluşan çok ajanlı karar simülasyonu.
- Round-based debate yapısı ile ajanların birbirlerinin önceki mesajlarını dikkate alması.
- `POST /api/v1/scenarios/{id}/simulate` endpoint'i üzerinden detaylı simulation response üretilmesi.
- Response içinde `rounds`, `agent_outputs`, `final_score`, `final_decision`, `scenario_type`, `scenario_type_confidence` ve `agent_weights` alanlarının sunulması.
- React tabanlı Decision Cockpit arayüzünde senaryo seçimi, simülasyon başlatma, debate console, katkı grafiği ve executive report bölümlerinin gösterilmesi.
- PostgreSQL ve SQLAlchemy ile senaryoların, ajan çıktılarının ve final kararların kalıcı olarak saklanması.
- Alembic migration yapısı ile veritabanı şemasının yönetilmesi.
- pytest ile domain, API, schema ve veri pipeline testlerinin çalıştırılması.
- Agile datasetinin normalize edilmesi, doğrulanması ve analiz raporlarının hazırlanması.
- Docker Compose ile backend ve veritabanının birlikte çalıştırılabilmesi.

Proje kapsamı dışında bırakılan noktalar da bilinçli olarak belirlenmiştir. Sistem gerçek bir şirketin finans, ERP veya insan kaynakları sistemlerine canlı entegrasyon yapmaz. Kullanıcı kimlik doğrulama ve rol bazlı yetkilendirme bu teslimin ana hedefi değildir; demo ortamında anonim kullanım esas alınmıştır. LLM çıktıları karar destek amacıyla kullanılır, nihai iş kararını kullanıcı verir. Ayrıca production deployment, ölçeklendirme, güvenlik sertleştirmesi ve kurumsal izleme altyapısı bu dönem projesinin sınırları dışında tutulmuştur.

## 1.2 Hedef Kullanıcılar

## 1.2 Hedef Kullanıcılar

Sistem, tek bir kullanıcı tipinden çok karar sürecine katılan farklı roller düşünülerek tasarlanmıştır. Bu roller gerçek bir kurum içindeki yönetici, finans sorumlusu, insan kaynakları/operasyon yöneticisi ve karar analizi yapan ekip gibi aktörleri temsil eder. Her rol sistemden farklı bir çıktı beklediği için arayüz ve backend response yapısı yalnızca nihai kararı değil, kararın gerekçelerini ve sürecin izlerini de taşır.

Üst düzey yönetici (stratejik karar verici), yatırım ya da proje kararının kurum geneline etkisini hızlıca görmek ister. Bu nedenle sistemden **final decision**, **final score** ve **CEO perspektifinden stratejik yorum** bekler.

Finans sorumlusu (CFO / bütçe kontrol rolü), bütçe uygunluğu, beklenen ROI ve risk dengesini detaylı incelemek ister. Bu rol için sistemin çıktısı; **CFO agent analizi**, **risk ayarlı yorum** ve **finansal gerekçeleri** açıkça sunmalıdır.

HR / operasyon yöneticisi (ekip kapasitesi ve uygulanabilirlik sorumlusu), takımın hazırlık düzeyini, işe alım ihtiyacını ve operasyonel yükü görmek ister. Bu nedenle sistem, **HR agent analizi** ile birlikte **team readiness** değerlendirmesini anlaşılır şekilde vermelidir.

Karar analisti / proje ekibi (karar sürecini inceleyen ekip üyesi), ajanların hangi gerekçelerle sonuca vardığını adım adım takip etmek ister. Bu rol için sistem; **tur bazlı tartışma akışı (round-based debate)**, **agent outputs** ve gerektiğinde özetlenmiş bir **executive report** sağlamalıdır.

Ders / demo değerlendiricisi (projenin teknik çıktısını değerlendiren kişi), sistemin backend, frontend, veri ve test parçalarının birlikte çalıştığını görmek ister. Bu nedenle beklenen çıktılar; **çalışan demo**, **örnek API response’ları**, **test sonuçları** ve **raporlanmış mimari** kanıtlarıdır.

Bu kullanıcı profilleri sistemin arayüz tasarımını doğrudan etkilemiştir. Sadece final kararın gösterilmesi yeterli görülmemiş; her ajanın gerekçesi, güven değeri ve hangi tartışma turunda üretildiği bilgisi de UI’a taşınmıştır. Böylece karar çıktısı daha şeffaf ve savunulabilir hâle getirilmiştir.

## 1.3 Kullanılan Teknolojiler ve Araçlar

Projede backend, frontend, veritabanı, test, veri bilimi ve proje yönetimi için farklı araçlar birlikte kullanılmıştır. Teknoloji seçimi yapılırken ders kapsamındaki yazılım mühendisliği beklentileri, katmanlı mimari, test edilebilirlik ve demo sırasında çalıştırılabilirlik dikkate alınmıştır.

| Kategori | Teknoloji / Araç | Açıklama / Kullanım Amacı |
|---|---|---|
| Programlama Dili | Python, TypeScript | Python backend ve veri pipeline tarafında; TypeScript frontend arayüzünde kullanıldı. |
| Backend Çatısı | FastAPI | REST API endpointleri, request/response yönetimi ve Swagger dokümantasyonu için kullanıldı. |
| Frontend Çatısı | React + Vite | Decision Cockpit arayüzünün geliştirilmesi için kullanıldı. |
| UI ve Stil | Tailwind CSS, Lucide React, Recharts, Framer Motion | Panel düzeni, ikonlar, grafikler ve arayüz animasyonları için kullanıldı. |
| ORM | SQLAlchemy Async | Repository katmanında veritabanı erişimini ORM üzerinden yürütmek için kullanıldı. |
| Veritabanı | PostgreSQL | Senaryo, ajan çıktısı ve final karar kayıtlarının kalıcı saklanması için kullanıldı. |
| Migration | Alembic | Veritabanı şema değişikliklerini yönetmek için kullanıldı. |
| Test Çatısı | pytest, pytest-asyncio, httpx | Domain, API, schema ve veri pipeline testleri için kullanıldı. |
| Konteyner | Docker Compose | Backend ve PostgreSQL servislerini birlikte çalıştırmak için kullanıldı. |
| AI / LLM | Ollama, LangChain OpenAI adapter | Opsiyonel LLM destekli reasoning zenginleştirme için kullanıldı. |
| Veri İşleme | pandas, openpyxl | Agile datasetini okuma, normalize etme ve analiz etme süreçlerinde kullanıldı. |
| Proje Yönetimi | Jira Kanban | Görevlerin ekip içinde takip edilmesi ve durum geçişlerinin yönetilmesi için kullanıldı. |
| Sürüm Kontrolü | Git, GitHub, Pull Request | Feature branch, code review, CI ve merge süreçleri için kullanıldı. |
| CI/CD | GitHub Actions | Pull requestlerde otomatik test çalıştırmak için kullanıldı. |

Bu teknoloji seti sayesinde proje yalnızca çalışan bir demo uygulaması olarak değil, aynı zamanda sürdürülebilir ve test edilebilir bir yazılım ürünü olarak yapılandırılmıştır. Backend tarafında Clean Architecture yaklaşımıyla domain kuralları framework detaylarından ayrılmış, frontend tarafında ise backend response sözleşmesine bağlı bir cockpit ekranı geliştirilmiştir.

---

# 4. Sürüm Kontrolü - Git ve GitHub

Bu projede sürüm kontrolü Git ve GitHub üzerinden yürütülmüştür. Geliştirme sürecinde doğrudan `main` branch üzerinde çalışmak yerine, özellik bazlı branch'ler açılmış ve değişiklikler pull request süreciyle ana koda dahil edilmiştir. Bu yöntem özellikle backend, frontend ve veri bilimi görevlerinin aynı repository içinde ilerlemesi nedeniyle gerekli olmuştur. Çünkü bir tarafta FastAPI backend sözleşmesi değişirken, diğer tarafta React arayüzü bu response alanlarına bağlanmış; veri bilimi tarafında ise dataset normalization ve validation dosyaları geliştirilmiştir.

GitHub repository adresi:

```text
https://github.com/multi-agent-decision-engine/ai-decision-ecosystem
```

Bu bölümde repository yapısı, README içeriği, branch/pull request düzeni ve code review süreci açıklanmıştır. Raporun Word hâlinde ilgili yerlere GitHub arayüzünden alınan ekran görüntüleri eklenecektir.

## 4.1 GitHub Repository Yapısı

Repository, backend, frontend, veri pipeline, testler, migration dosyaları ve rapor dokümanlarını aynı proje altında toplayacak şekilde düzenlenmiştir. Klasör yapısı incelendiğinde sistemin yalnızca API kodundan oluşmadığı, aynı zamanda frontend cockpit, gerçek veri hazırlığı, Docker çalıştırma dosyaları ve rapor kanıtları gibi teslim bileşenlerini de içerdiği görülür.

| Klasör / Dosya | Açıklama |
|---|---|
| `app/` | FastAPI backend uygulamasının ana kaynak kodlarını içerir. Domain, application, infrastructure ve presentation katmanları bu klasör altında ayrılmıştır. |
| `frontend/` | React, Vite ve TypeScript ile geliştirilen Decision Cockpit arayüzünü içerir. Scenario listesi, simulation başlatma, debate console ve executive report panelleri bu bölümde yer alır. |
| `tests/` | pytest ile yazılmış domain, API, schema snapshot, dataset validation ve LLM entegrasyon testlerini içerir. |
| `docs/` | Mimari açıklamalar, backend simulation contract, demo notları, workflow dokümanları ve rapor için kullanılan kanıt dosyalarını içerir. |
| `data/` | Gerçek dataset dosyaları ve normalize edilmiş veri çıktıları için kullanılır. |
| `scripts/` | Dataset normalization, validation, evaluation, training ve demo amaçlı yardımcı scriptleri içerir. |
| `reports/` | Veri analizi ve model/training sonuç raporlarının tutulduğu klasördür. |
| `alembic/` | PostgreSQL veritabanı migration dosyalarını içerir. |
| `.github/` | GitHub Actions ve repository iş akışları için kullanılan konfigürasyonları içerir. |
| `docker-compose.yml` | Backend ve PostgreSQL servislerinin birlikte çalıştırılmasını sağlar. |
| `Dockerfile` | Backend uygulamasının container image olarak build edilmesi için kullanılır. |
| `requirements.txt` | Backend Python bağımlılıklarını listeler. |
| `README.md` | Projenin genel tanıtımı, kurulum adımları, API endpointleri, mimari yaklaşımı ve demo komutlarını içerir. |

**Eklenecek Görsel:** GitHub repository ana sayfasının ekran görüntüsü bu bölümün altına eklenecektir. Görselde `app/`, `frontend/`, `tests/`, `docs/`, `scripts/`, `data/` ve `README.md` gibi temel öğelerin görünmesi yeterlidir.

## 4.2 README Dosyası

Repository içindeki `README.md`, projenin hızlıca anlaşılması ve çalıştırılması için ana giriş dokümanı olarak kullanılmıştır. README içerisinde sistemin amacı, kullanılan teknolojiler, local kurulum, Docker ile çalıştırma, API endpointleri, detailed simulation response alanları, scenario input contract ve test komutları açıklanmıştır.

README dosyasında özellikle şu bilgiler yer alır:

- Projenin multi-agent karar destek sistemi olarak amacı.
- Backend teknolojileri: FastAPI, PostgreSQL, SQLAlchemy, Alembic.
- Frontend teknolojileri: React, Vite, TypeScript.
- Local LLM desteği: Ollama üzerinde çalışan Qwen modeli ile reasoning zenginleştirme.
- Docker Compose ile backend ve veritabanını başlatma adımları.
- `POST /api/v1/scenarios`, `GET /api/v1/scenarios`, `POST /api/v1/scenarios/{id}/simulate` gibi temel API endpointleri.
- Detailed simulation response içinde kullanılan `rounds`, `agent_outputs`, `final_score`, `final_decision`, `scenario_type` ve `agent_weights` alanları.
- Testlerin `pytest` ile çalıştırılması.
- Demo için kullanılabilecek örnek `curl` komutları.

README'nin projedeki rolü sadece kurulum talimatı vermek değildir. Aynı zamanda backend ile frontend arasındaki sözleşmenin özetini de sunar. Örneğin frontend'in debate console ekranında kullandığı `rounds[].messages[]` alanı ve final report için kullanılan `final_score` / `final_decision` alanları README ve `docs/backend_simulation_contract.md` üzerinden açıklanmıştır.

**Eklenecek Görsel:** GitHub üzerinde açılmış `README.md` dosyasından bir ekran görüntüsü eklenecektir. Görselde proje başlığı, teknoloji bilgileri ve API endpoint özetinin görünmesi tercih edilir.

## 4.3 GitHub Tarafı

GitHub tarafında geliştirme branch yapısı özellik bazlı ilerlemiştir. Her önemli geliştirme ayrı bir `feature/...` branch üzerinde yapılmış, daha sonra pull request ile `main` branch'e alınmıştır. Bu sayede backend sözleşmesi, frontend cockpit, veri pipeline ve LLM entegrasyonu gibi parçalar birbirinden ayrılmış şekilde takip edilebilmiştir.

Repository'de kullanılan önemli branch örnekleri şunlardır:

| Branch | Amaç |
|---|---|
| `main` | Teslim edilebilir ve merge edilmiş son kodun bulunduğu ana branch. |
| `develop` | Bazı geliştirme denemeleri ve ara entegrasyonlar için kullanılan geliştirme branch'i. |
| `feature/discussion-orchestrator` | Ajanların tur bazlı tartışma yapısını geliştiren branch. |
| `feature/ai-decision-cockpit` | React tabanlı ilk frontend cockpit çalışmasını içeren branch. |
| `feature/post-pr6-frontend-backend-integration` | Frontend'in gerçek backend simulation API'sine bağlandığı branch. |
| `feature/backend-simulation-contract` | Detailed simulation response schema, backend contract ve snapshot testlerini içeren branch. |
| `feature/real-data-helin` | Gerçek veri çalışmasının ilk aşamalarını içeren branch. |
| `feature/data-pipeline-final-helin` | Veri normalization, validation ve loader tarafının final hâlini içeren branch. |
| `feature/phase2-calibration-kickoff` | DatasetLoader ile AgentCalibrator entegrasyonunu başlatan branch. |
| `feature/llm-agent-integration` | Local LLM destekli reasoning zenginleştirme katmanını ekleyen branch. |

Pull request geçmişinde backend, frontend ve veri bilimi katkıları ayrı PR'lar üzerinden izlenebilir. Örneğin:

| PR | Başlık | Branch | Durum |
|---|---|---|---|
| #6 | `feat(frontend): add interactive agent debate console` | `feature/ai-decision-cockpit` | Merged |
| #7 | `feat(frontend): connect cockpit to backend simulation API` | `feature/post-pr6-frontend-backend-integration` | Merged |
| #8 | `feat(backend): detailed round-based simulation contract + schema snapshot tests` | `feature/backend-simulation-contract` | Merged |
| #12 | `Feature: Data Evaluation and Loader Final` | `feature/data-pipeline-final-helin` | Merged |
| #13 | `feat(phase2): DatasetLoader -> AgentCalibrator runtime integration with honest baselines` | `feature/phase2-calibration-kickoff` | Merged |
| #14 | `Feature/llm agent integration` | `feature/llm-agent-integration` | Merged |

Bu PR akışı proje ilerledikçe modüllerin birbirine bağlanmasını daha kontrollü hâle getirmiştir. Önce ajan ve backend response sözleşmesi netleşmiş, ardından frontend bu sözleşmeye bağlanmış, daha sonra veri pipeline ve LLM reasoning katmanı eklenmiştir.

**Eklenecek Görseller:**

- GitHub `Branches` sekmesi ekran görüntüsü.
- GitHub `Pull requests` listesi ekran görüntüsü.
- Commit history ekran görüntüsü.

## 4.4 Pull Request ve Code Review Süreci

Projede tamamlanan geliştirmeler `main` branch'e doğrudan gönderilmemiş, pull request süreciyle gözden geçirilmiştir. PR açılırken yapılan değişikliğin amacı, etkilenen dosyalar ve çalıştırılan testler açıklanmıştır. Özellikle backend response sözleşmesini etkileyen değişikliklerde test komutları ve kabul kriterleri PR açıklamalarına eklenmiştir.

Pull request sürecinde izlenen genel adımlar şöyledir:

1. Jira veya ekip görev planında iş kalemi belirlenir.
2. İlgili geliştirme için feature branch açılır.
3. Kod değişikliği yapıldıktan sonra yerelde testler çalıştırılır.
4. Branch GitHub'a push edilir ve pull request açılır.
5. PR üzerinde dosya değişiklikleri incelenir.
6. Gerekirse yorumlarla düzeltme istenir.
7. CI testleri başarılı olduktan sonra PR merge edilir.

Bu süreçte özellikle üç tür kontrol yapılmıştır. İlk kontrol, kodun mimari katmanlara uygun olup olmadığıdır. Örneğin domain katmanının doğrudan FastAPI veya SQLAlchemy detaylarına bağımlı olmaması beklenmiştir. İkinci kontrol, frontend-backend response sözleşmesinin bozulmamasıdır. Bu yüzden detailed simulation response için Pydantic schema ve OpenAPI snapshot testleri eklenmiştir. Üçüncü kontrol ise veri pipeline tarafında normalize edilen datasetin doğrulanabilir olmasıdır.

Örnek olarak PR #8, backend simulation contract açısından önemli bir PR'dır. Bu PR ile `/api/v1/scenarios/{id}/simulate` endpoint'i `rounds`, `agent_outputs`, `final_score`, `final_decision`, `scenario_type` ve `agent_weights` gibi alanları dönecek şekilde genişletilmiştir. PR #7 ise frontend'in mock veriden çıkıp gerçek backend simulation API'sine bağlandığı adımdır. PR #14'te ise LLM reasoning integration eklenmiş, ancak LLM'in karar skorunu değiştirmemesi için fallback ve contradiction guard uygulanmıştır.

Code review süreci proje için yalnızca hata bulma aşaması olarak görülmemiştir. Aynı zamanda ekip içinde backend sözleşmesinin, frontend beklentilerinin ve veri hazırlama kararlarının netleştiği bir koordinasyon noktası olmuştur. Bu nedenle rapora eklenecek PR ekran görüntülerinde yalnızca merge durumu değil, yorumlar, CI sonucu ve branch bağlantısı da gösterilecektir.

**Eklenecek Görseller:**

- PR #8 veya PR #14 detay ekranı.
- PR içinde `Files changed` sekmesinde yapılan yorumlardan örnek.
- CI/checks bölümünün başarılı olduğunu gösteren ekran görüntüsü.
- Merge edilmiş PR durumunu gösteren ekran görüntüsü.

---

## Bölüm 4 İçin Toplanacak Görsel Listesi

Rapor formatı bu bölümde görsel istediği için aşağıdaki ekran görüntüleri ayrıca toplanmalıdır:

| Görsel | Nereden Alınacak | Önerilen Dosya Adı |
|---|---|---|
| Repo ana sayfası | GitHub repository ana ekranı | `docs/report_assets/github/01_repo_home.png` |
| Branch listesi | GitHub `Branches` sekmesi | `docs/report_assets/github/02_branches.png` |
| Commit history | GitHub `Commits` görünümü | `docs/report_assets/github/03_commit_history.png` |
| Pull request listesi | GitHub `Pull requests` sekmesi | `docs/report_assets/github/04_pr_list.png` |
| Örnek PR detay | PR #8 veya PR #14 conversation ekranı | `docs/report_assets/github/05_pr_detail.png` |
| Code review yorumu | PR `Files changed` ekranı | `docs/report_assets/github/06_review_comment.png` |
| CI sonucu | PR checks / GitHub Actions ekranı | `docs/report_assets/github/07_ci_success.png` |
