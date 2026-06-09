"""Tartisma turleri arasinda gozle gorulur dinamik uretmek icin yardimcilar.

Bu modul tek bir hedefe hizmet eder: agent'lar arasinda **gozlemlenebilir**
fikir hareketleri yaratmak. Mevcut agent'lar zaten cross-analysis yapiyor ama
tetikleyici esikleri (orn. `risk > 7`, `team_impact < 3`) cok kati oldugu icin
ortalama bir senaryoda hicbir agent fikir guncellemiyor; Round 2 ile Round 3
metinleri ozdes oluyor.

`apply_convergence_pressure` her agent'in Round 2+ analizinin sonunda cagrilir
ve kendi confidence'ini akran ortalamasina dogru `pressure_weight` orani kadar
ceker. Bu, **karari** bozmaz (decision aggregator ayni mekanikta calisir),
ancak Round 2/3'te gorulur **hareket** uretir.
"""
from __future__ import annotations

from app.domain.models import AgentMessage


def apply_convergence_pressure(
    confidence: float,
    previous_messages: list[AgentMessage] | None,
    self_agent_name: str,
    pressure_weight: float = 0.15,
) -> tuple[float, str | None]:
    """Confidence'i son turdeki akran ortalamasina dogru ceker.

    Args:
        confidence: Agent'in mevcut (kendi analizi sonrasi) confidence degeri.
        previous_messages: Onceki turlerin mesajlari (None ya da bos olabilir).
        self_agent_name: Agent'in adi ("CEO", "CFO", "HR"). Kendi mesajlari
            ortalamaya dahil edilmez.
        pressure_weight: 0..1 araliginda; 0 hicbir etki, 1 tam akran ortalamasi.
            Varsayilan 0.15: ufak ama gozle gorulebilir hareket.

    Returns:
        (new_confidence, optional_note) - note None degilse reasoning'e eklenir.
    """
    if not previous_messages:
        return confidence, None

    # Yalniz en son turun mesajlarini dikkate al (her tur peer'lara taze sinyal).
    last_round = max(m.round_number for m in previous_messages)
    peers = [
        m for m in previous_messages
        if m.round_number == last_round and m.agent != self_agent_name
    ]
    if not peers:
        return confidence, None

    peer_mean = sum(p.confidence for p in peers) / len(peers)
    delta = peer_mean - confidence
    new_conf = confidence + delta * pressure_weight

    note: str | None = None
    if abs(delta) >= 0.10:
        direction = "yukseldi" if delta > 0 else "dustu"
        note = (
            f"Ekip ortalama guveni %{int(peer_mean * 100)}; bu nedenle "
            f"kendi guvenim {direction} (yaklasma etkisi {delta:+.2f})."
        )

    return new_conf, note


def maybe_soften_stance(
    stance: str,
    confidence: float,
    previous_messages: list[AgentMessage] | None,
    self_agent_name: str,
    flip_threshold: float = 0.42,
) -> tuple[str, str | None]:
    """Confidence belirli bir esigin altina dustuyse stance'i nutr'a ceker.

    Mevcut kodda stance shift sadece "tum digerleri karsit" gibi ekstrem
    durumlarda calisiyor. Bu fonksiyon, akran baskisi nedeniyle confidence
    iyice dustugunde "ben artik emin degilim" cevirmesini saglar.

    Sadece extreme stance'leri (support/oppose) nutr'a ceker; nutr olan agent
    burada degisim gormez.

    Returns:
        (new_stance, optional_note)
    """
    if not previous_messages:
        return stance, None
    if stance == "neutral":
        return stance, None
    if confidence >= flip_threshold:
        return stance, None

    note = (
        f"Akran baskisi sonrasi guven %{int(confidence * 100)}'a dusunce "
        f"tutum {stance} -> neutral olarak revize edildi."
    )
    return "neutral", note
