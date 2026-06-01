# Data Science Overview

Bu dosya, veri bilimiyle ilgili daginik notlari raporda kullanilabilir tek bir
ozete indirir. Ayrintili eski notlar `docs/data_science/archive/` altinda
saklanir.

## Amac

Projede veri bilimi katmaninin amaci, multi-agent karar mekanizmasini yalnizca
sabit kurallarla degil, veriyle desteklenen skorlar ve kalibrasyon yaklasimiyla
guclendirmektir. Bu nedenle sistemde uc ana hedef belirlendi:

- Karar senaryolarini tutarli ozelliklere ayirmak.
- CEO, CFO ve HR agent skorlarini veriyle daha dengeli hale getirmek.
- Gercek proje verilerinden raporda savunulabilir ornekler uretmek.

## Veri Kaynaklari

Calismada iki veri hattindan yararlanildi:

- Gercek veya yari-gercek Agile proje verileri.
- Model egitimi ve demo icin sentetik senaryo uretimi.

Gercek veri tarafinda sprint, gorev, sure, durum, oncelik ve rol bilgileri
karar destek problemine uygun ozelliklere cevrildi. Sentetik veri tarafinda ise
farkli butce, risk, ekip kapasitesi ve beklenen getiri kombinasyonlariyla test
senaryolari olusturma plani hazirlandi.

## Ozellik Tasarimi

Karar motoru icin kullanilan temel ozellik aileleri:

- Finansal sinyaller: butce, beklenen getiri, maliyet riski.
- Stratejik sinyaller: pazar etkisi, uzun vadeli deger, rekabet avantaji.
- Operasyonel sinyaller: ekip kapasitesi, uygulanabilirlik, zaman baskisi.
- Insan kaynagi sinyalleri: rol ihtiyaci, ekip yuku, yetkinlik eksigi.

Bu ozellikler agent bazli skorlamaya temel olur. CEO daha cok stratejiye, CFO
finansal dengeye, HR ise ekip ve operasyonel kapasiteye agirlik verir.

## Modelleme Yaklasimi

Proje raporu icin modelleme kismi asagidaki seviyede konumlandirilir:

- Ilk surumde kural tabanli karar motoru calisir.
- Veri bilimi katmani, bu kararlarin daha sonra egitilebilir hale gelmesi icin
  ozellik seti ve etiket mantigini tanimlar.
- ML siniflandirma yaklasimi `APPROVE`, `REVISE`, `REJECT` kararlarini tahmin
  edecek sekilde planlanir.
- Agent kalibrasyonu, gecmis senaryolardaki sonuc basarimina gore skor
  agirliklarini iyilestirme hedefi tasir.

## Outcome Based Reinforcement Learning Notu

Outcome based RL fikri, sistemin verdigi kararlarin ileride gercek sonuclarla
geri beslenmesi uzerine kuruludur. Ornegin bir yatirim karari sonrasi maliyet,
gecikme veya ekip etkisi takip edilirse, ajan agirliklari sonraki kararlar icin
daha gercekci ayarlanabilir.

Bu proje kapsaminda tam RL egitimi teslim kapsaminda ana hedef degildir; ancak
raporda gelecek calisma olarak savunulabilir bir gelisim yoludur.

## Egitim Stratejisi

Planlanan egitim akisi:

1. Senaryo verilerini normalize etmek.
2. Ozellikleri agent bakis acilarina gore ayirmak.
3. Baslangic etiketlerini uzman/kural tabanli kararlarla olusturmak.
4. ML siniflandirma modeliyle karar tahmini yapmak.
5. Sonuclara gore agent skor agirliklarini kalibre etmek.

Bu yapi, projenin sadece demo uygulamasi degil, veriyle gelistirilebilir bir
karar destek sistemi oldugunu gostermek icin raporda kullanilabilir.

## Rapor Icin Kisa Yorum

Veri bilimi calismasi, projenin karar verme mekanizmasina olculebilir bir temel
kazandirir. Backend tarafindaki agent skorlarinin hangi gerekceyle uretildigi,
hangi ozelliklerden beslendigi ve gelecekte nasil egitilebilir hale gelecegi bu
bolumle aciklanir.
