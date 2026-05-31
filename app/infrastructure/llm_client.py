"""LLM istemcisi somut implementasyonları.

Domain port'u (`app.domain.agents.llm_port.LLMClient`) burada concrete
sınıflarla karşılanır:

- `OllamaLLMClient` — production, `call_llm` ile Ollama'yı çağırır
- `StubLLMClient` — test/demo, deterministik yanıtlar döner

Domain katmanı bu modülü import etmez; yalnızca dış katmanlar (factory,
testler, demolar) bu somut sınıfları kullanır.
"""

from __future__ import annotations

# Re-export domain port öğelerini buradan da erişilebilir kıl (geriye dönük
# import uyumluluğu için; eski kod `from app.infrastructure.llm_client import
# LLMClient` yazıyorsa kırılmasın).
from app.domain.agents.llm_port import LLMClient, LLMUnavailableError  # noqa: F401


class StubLLMClient:
    """Testler için deterministik istemci.

    Verilen `responses` listesini sırayla döner; tükenirse `default_response`.
    Çağrı sayısı ve son prompt `calls` listesinde saklanır.
    """

    def __init__(
        self,
        responses: list[str] | None = None,
        default_response: str = "STUB_LLM_OK",
        raise_on_call: Exception | None = None,
    ) -> None:
        self._responses = list(responses or [])
        self._default = default_response
        self._raise = raise_on_call
        self.calls: list[dict] = []

    def complete(self, prompt: str, *, agent_name: str, scenario_name: str) -> str:
        self.calls.append(
            {"prompt": prompt, "agent_name": agent_name, "scenario_name": scenario_name}
        )
        if self._raise is not None:
            raise self._raise
        if self._responses:
            return self._responses.pop(0)
        return self._default


class OllamaLLMClient:
    """Production istemci — `app.infrastructure.llm.call_llm` üzerinden Ollama'yı çağırır.

    `call_llm` zaten timing/loglamayı `llm_logger` ile yapıyor; biz de
    network/timeout hatalarını `LLMUnavailableError`'a çeviriyoruz.
    """

    def __init__(self, model_name: str | None = None) -> None:
        self._model_name = model_name

    def complete(self, prompt: str, *, agent_name: str, scenario_name: str) -> str:
        # Lazy import: LangChain/Ollama bağımlılığı yalnızca runtime'da gerek.
        try:
            from app.infrastructure.llm import call_llm
        except ImportError as exc:  # pragma: no cover
            raise LLMUnavailableError(f"LLM bağımlılığı yüklenemedi: {exc}") from exc

        try:
            return call_llm(
                prompt=prompt,
                agent_name=agent_name,
                scenario_name=scenario_name,
                model_name=self._model_name,
            )
        except Exception as exc:
            raise LLMUnavailableError(
                f"LLM çağrısı başarısız ({agent_name} / {scenario_name}): {exc}"
            ) from exc
