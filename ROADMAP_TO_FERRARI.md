# 🏎️ Ferrari Motor Takma Planı (Transformation Roadmap)

Bu belge, kural tabanlı (rule-based) eski yapıyı, LLM tabanlı (AI-driven) modern bir multi-agent sistemine dönüştürme planını içerir.

## Aşama 1: Beyin Nakli (Infrastructure Integration) -  ACİL
- [x] `requirements.txt` güncellendi (LangChain community eklendi).
- [x] `app/infrastructure/llm.py` oluşturuldu. (Local Qwen / Ollama entegrasyonu hazır).
- [ ] **[JIRA-01]** `.env` yapılandırması (Lokal URL ve Model ismi).
- [ ] **[JIRA-02]** `PromptTemplate` yapısının kurulması. Her agent'ın kişiliği (persona) burada tanımlanacak.

## Aşama 2: Agent'ların Uyanışı (Persona Implementation)
Artık `if risk > 5` yok. Agent'lar konuşacak.
- [ ] **[JIRA-03]** **CEO Agent:**
  - System Prompt: "Sen vizyoner, risk alan ama stratejik düşünen, Steve Jobs vari bir CEO'sun."
  - Input: Senaryo metni + ROI verisi.
  - Output: Stratejik uyum analizi (Metin + Skor).
- [ ] **[JIRA-04]** **CFO Agent:**
  - System Prompt: "Sen cimri, detaycı, her kuruşu sayan ve riskten nefret eden bir CFO'sun."
  - Input: Bütçe + ROI + Piyasa Riski.
  - Output: Finansal sürdürülebilirlik analizi.
- [ ] **[JIRA-05]** **HR Agent:**
  - System Prompt: "Sen insan odaklı, tükenmişlikten korkan, kültür koruyucusu bir İK yöneticisisin."
  - Input: Ekip durumu + İş yükü.
  - Output: Organizasyonel kapasite analizi.

## Aşama 3: Meydan Muharebesi (Orchestrator V2)
Agent'lar birbirini duyacak.
- [ ] **[JIRA-06]** **Debate Loop (Tartışma Döngüsü):**
  - Round 1: Herkes fikrini söyler.
  - Round 2 (Rebuttal): CFO'nun "Para yok" dediğini CEO görür ve "Yatırımcı buluruz" der.
- [ ] **[JIRA-07]** **Chairman (Yönetim Kurulu Başkanı):**
  - Tüm bu kaosu alıp tek bir karar metninde toplayan "Sentezleyici Agent".

## Aşama 4: Raporlama ve Görsellik
- [ ] **[JIRA-08]** Karar raporuna "Neden kabul edildi?", "Hangi riskler göze alındı?" bölümlerinin eklenmesi.
- [ ] **[JIRA-09]** Agent'ların birbirine yaptığı alıntıların rapora yansıması.

---
**Teknolojik Altyapı:**
- **Model:** GPT-4 Turbo veya GPT-3.5 Turbo (Maliyet/Performans dengesine göre).
- **Format:** JSON Mode (Agent'ların yapısal çıktı vermesi için).
- **Framework:** LangChain (Prompt yönetimi için).
