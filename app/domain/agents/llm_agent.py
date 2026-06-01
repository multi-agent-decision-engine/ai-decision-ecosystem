"""LLM-Augmented Agent wrapper.

`Agent` arayüzünü implement eder; içinde sarmaladığı `base_agent`'ı çalıştırır
(stance / confidence / metrics deterministik kalır) ve `reasoning` alanını
LLM çıktısıyla zenginleştirir. LLM erişilemezse base agent çıktısına döner.

Tasarım kararları:
- Stance/confidence/metrics base agent'tan gelir → AgentMessage sözleşmesi
  ve `tests/test_simulation_schema_snapshot.py` invariant'ları korunur.
- LLM yalnız reasoning'i zenginleştirir → hallucination decision logic'ini
  kirletemez.
- Round 2+ prompt'u önceki tüm ajan mesajlarını + persona one-liner'larını
  içerir → ajanlar birbirine "kim olduğunu" bilerek yanıt verir.
- LLM çıktısı `_sanitize_llm_output` ile markdown/JSON noise'undan temizlenir.
- Base stance ile LLM metni açıkça çelişiyorsa LLM çıktısı kullanılmaz;
  base agent mesajına geri dönülür.
"""

from __future__ import annotations

import re

from app.domain.agents.base import Agent
from app.domain.agents.prompts import (
    AGENT_ONELINER,
    AGENT_PERSONA_LOOKUP,
)
from app.domain.agents.llm_port import LLMClient, LLMUnavailableError
from app.domain.models import AgentMessage, ScenarioInput


def _agent_short_name(agent: Agent) -> str:
    """`CEOAgent` -> `CEO`."""
    name = agent.__class__.__name__
    if name.endswith("Agent"):
        name = name[:-5]
    return name.upper()


def _format_prior_messages(previous_messages: list[AgentMessage] | None) -> str:
    if not previous_messages:
        return "(önceki mesaj yok — bu 1. tur)"
    lines = []
    for msg in previous_messages:
        persona_hint = AGENT_ONELINER.get(msg.agent, msg.agent)
        lines.append(
            f"- Tur {msg.round_number} | {msg.agent} [{persona_hint}] "
            f"(stance: {msg.stance}, confidence: {msg.confidence:.2f}):\n"
            f"  {msg.reasoning}"
        )
    return "\n".join(lines)


def _build_prompt(
    agent_name: str,
    system_prompt: str,
    scenario_inputs: ScenarioInput,
    base_message: AgentMessage,
    previous_messages: list[AgentMessage] | None,
) -> str:
    prior_block = _format_prior_messages(previous_messages)
    has_prior = bool(previous_messages)

    cross_ref_instruction = (
        "(c) Önceki mesajlardaki **en güçlü** endişeyi veya argümanı tanımla; "
        "kendi alanından gelen veriyle ya **somut şekilde pekiştir** ya da "
        "**açıkça karşı çık** (\"katılıyorum çünkü...\" veya "
        "\"katılmıyorum çünkü...\" gibi)."
        if has_prior
        else "(c) Bu 1. tur olduğu için sadece kendi analizini sun; "
             "diğer ajanların görüşünü beklediğini kısaca belirt."
    )

    return (
        f"{system_prompt}\n\n"
        f"## Senaryo\n"
        f"isim: {scenario_inputs.name}\n"
        f"açıklama: {scenario_inputs.description}\n"
        f"bütçe (milyon USD): {scenario_inputs.budget_million_usd}\n"
        f"beklenen ROI (%): {scenario_inputs.expected_roi_percent}\n"
        f"risk seviyesi (1-10): {scenario_inputs.risk_level}\n"
        f"takım hazırlığı (1-10): {scenario_inputs.team_readiness}\n\n"
        f"## Domain Mantığının Hesapladığı Yapılandırılmış Analiz\n"
        f"stance: {base_message.stance}\n"
        f"confidence: {base_message.confidence:.2f}\n"
        f"metrics: {base_message.metrics}\n\n"
        f"## Önceki Tartışma\n"
        f"{prior_block}\n\n"
        f"## Görevin\n"
        f"Sen {agent_name}'sun. 3-5 cümlelik **birinci tekil şahıs** bir gerekçe yaz; "
        f"şu üç noktayı mutlaka karşıla:\n"
        f"(a) Stance'ini ({base_message.stance}) kendi karakterinle açıkla. "
        f"Yapılandırılmış analizdeki stance ile **çelişme**; ona dilsel zenginlik kat.\n"
        f"(b) Karara etki eden **en kritik sayısal sürücüyü** (ROI, risk, "
        f"team_readiness, bütçe vb.) somut sayıyla anarak göster.\n"
        f"{cross_ref_instruction}\n\n"
        f"Çıktı: SADECE düz metin gerekçe — başlık YOK, JSON YOK, "
        f"madde listesi YOK, markdown YOK. En fazla 5 cümle."
    )


# --- Output cleaning & guards ---------------------------------------------


_CODE_FENCE_RE = re.compile(r"```[a-zA-Z]*\n?")
_MD_HEADER_RE = re.compile(r"^\s*#{1,6}\s+.*$", re.MULTILINE)
_BULLET_RE = re.compile(r"^\s*[-*•]\s+", re.MULTILINE)
_QUOTE_RE = re.compile(r'^\s*"reasoning"\s*:\s*"(.*)"\s*$', re.DOTALL)


def _sanitize_llm_output(text: str) -> str:
    """LLM çıktısından markdown/JSON noise'unu temizle.

    - Üç apostrof code fence'leri kaldırır.
    - "reasoning": "..." JSON wrapper varsa içeriğini çıkarır.
    - Markdown başlıklarını (`#`, `##`) düz metne çevirir.
    - Madde işaretlerini (`-`, `*`, `•`) kaldırır.
    - Baş ve sondaki boşlukları kırpar.
    """
    if not text:
        return ""

    cleaned = text.strip()

    # JSON wrapper: {"reasoning": "..."}
    json_match = _QUOTE_RE.match(cleaned)
    if json_match:
        cleaned = json_match.group(1)

    cleaned = _CODE_FENCE_RE.sub("", cleaned)
    cleaned = _MD_HEADER_RE.sub("", cleaned)
    cleaned = _BULLET_RE.sub("", cleaned)
    cleaned = re.sub(r"\n{3,}", "\n\n", cleaned)
    return cleaned.strip()


_POSITIVE_TOKENS = {
    # destek anlamı taşıyan TR/EN kelimeler
    "destekliyorum", "destekliyoruz", "onaylıyorum", "onaylıyoruz", "evet",
    "katılıyorum", "support", "approve", "go ahead", "ilerleyelim",
    "yatırımı yapalım",
}
_NEGATIVE_TOKENS = {
    # karşı çıkma anlamı taşıyan TR/EN kelimeler
    "reddediyorum", "reddediyoruz", "reddedelim", "reject", "karşıyım",
    "vetoyu", "veto", "imzalamam", "imzalamıyorum", "do not approve",
    "yatırımı durdural", "yatırımı erteleyelim", "iptal edelim",
}


def _detect_stance_contradiction(
    base_stance: str, reasoning_text: str
) -> bool:
    """LLM metni base stance ile açıkça çelişiyor mu?

    Heuristik (intentionally conservative): yalnız net karşıt sinyaller
    yakalanır, gri durumlar `False` döner. Frontend/analist için bayrak;
    karar geri alınmaz.
    """
    if not reasoning_text:
        return False
    lower = reasoning_text.lower()

    def contains_any(tokens: set[str]) -> bool:
        return any(tok in lower for tok in tokens)

    if base_stance == "support" and contains_any(_NEGATIVE_TOKENS):
        # support'tayız ama metin "reddediyorum" diyor
        if not contains_any(_POSITIVE_TOKENS):
            return True
    if base_stance == "oppose" and contains_any(_POSITIVE_TOKENS):
        if not contains_any(_NEGATIVE_TOKENS):
            return True
    if base_stance == "neutral" and (
        contains_any(_POSITIVE_TOKENS) or contains_any(_NEGATIVE_TOKENS)
    ):
        return True
    return False


# --- LLMAgent --------------------------------------------------------------


class LLMAgent(Agent):
    """Base agent çıktısını LLM ile zenginleştiren wrapper.

    Stance/confidence/metrics dokunulmaz; sadece `reasoning` alanı LLM çıktısıyla
    değiştirilir. LLM erişilemezse base agent'ın orijinal mesajı döner.
    """

    def __init__(
        self,
        base_agent: Agent,
        llm_client: LLMClient,
        system_prompt: str | None = None,
        agent_name: str | None = None,
    ) -> None:
        self.base_agent = base_agent
        self.llm_client = llm_client
        self._agent_name = agent_name or _agent_short_name(base_agent)
        self._system_prompt = system_prompt or AGENT_PERSONA_LOOKUP.get(
            self._agent_name,
            "Sen bir iş senaryosunu değerlendiren uzman bir profesyonelsin.",
        )

    def _build_reasoning_prompt(self, scenario_inputs: ScenarioInput) -> str:
        return self.base_agent._build_reasoning_prompt(scenario_inputs)

    def analyze(
        self,
        scenario_inputs: ScenarioInput,
        previous_messages: list[AgentMessage] | None = None,
    ) -> AgentMessage:
        base_message = self.base_agent.analyze(
            scenario_inputs,
            previous_messages=previous_messages,
        )

        prompt = _build_prompt(
            agent_name=self._agent_name,
            system_prompt=self._system_prompt,
            scenario_inputs=scenario_inputs,
            base_message=base_message,
            previous_messages=previous_messages,
        )

        try:
            raw_llm_text = self.llm_client.complete(
                prompt,
                agent_name=self._agent_name,
                scenario_name=scenario_inputs.name,
            )
        except LLMUnavailableError:
            return base_message

        sanitized = _sanitize_llm_output(raw_llm_text)
        if not sanitized:
            return base_message

        contradiction = _detect_stance_contradiction(
            base_message.stance, sanitized
        )
        if contradiction:
            return base_message

        metrics = dict(base_message.metrics)
        metrics["llm"] = {
            "source": self.llm_client.__class__.__name__,
            "fallback_used": False,
            "sanitized": raw_llm_text != sanitized,
            "stance_contradiction": False,
        }

        return AgentMessage(
            agent=base_message.agent,
            stance=base_message.stance,
            confidence=base_message.confidence,
            reasoning=sanitized,
            metrics=metrics,
            round_number=base_message.round_number,
        )
