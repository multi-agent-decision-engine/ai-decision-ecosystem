"""Domain port: LLM istemcisi arayüzü.

Clean Architecture'ın dependency rule'u: domain bilgi dış katmanlardan değil,
dış katmanlar domain'den **bağımlıdır**. LLM istemcisinin arayüzü burada
(domain) tanımlanır; somut sınıflar (`OllamaLLMClient`, `StubLLMClient`)
`app/infrastructure/llm_client.py` altında bu port'a implement edilir.

`LLMAgent` yalnız bu port'u tanır — dış katmana referans vermez.
"""

from __future__ import annotations

from typing import Protocol


class LLMUnavailableError(RuntimeError):
    """LLM çağrısı başarısız olduğunda fırlatılır (network, timeout, model down).

    `LLMAgent` bu hatayı yakalar ve base agent template'ine geri düşer.
    """


class LLMClient(Protocol):
    """LLM istemcisi sözleşmesi.

    Implementing classes must provide a synchronous `complete` method that
    returns the generated text. Hatalar `LLMUnavailableError` ile sarılmalı.
    """

    def complete(self, prompt: str, *, agent_name: str, scenario_name: str) -> str:
        """Prompt'u tamamlanmış metin olarak döndürür."""
        ...
