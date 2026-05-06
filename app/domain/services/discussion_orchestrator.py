from app.domain.models import AgentMessage, ScenarioInput
from app.domain.agents.base import Agent

class DiscussionOrchestrator:
    """
    Ajanlar arasındaki çok turlu tartışma (discussion) sürecini yöneten orkestratör sınıfı.
    
    Ajanların belirlenen tur sayısı kadar senaryoyu sıralı bir şekilde analiz etmesinden,
    önceki turlardaki veya aynı turdaki diğer ajanların mesajlarını (previous_messages)
    görebilmelerinden sorumludur.
    """

    def run_discussion(
        self,
        scenario: ScenarioInput,
        agents: list[Agent],
        rounds: int = 2
    ) -> list[AgentMessage]:
        """
        Belirtilen senaryo üzerinde ajanlar arasında tartışma sürecini başlatır ve yönetir.

        Her turda:
        1. Ajanlar sırayla senaryoyu analiz eder (`analyze()`).
        2. Kendisinden önce analiz yapan ajanların (mevcut tur dâhil) mesajlarını okur.
        3. Ürettikleri mesajlar `round_number` atanarak kaydedilir.

        Args:
            scenario: Tartışılacak senaryonun girdi verileri (ScenarioInput).
            agents: Tartışmaya katılacak ajanların (Agent) listesi.
            rounds: Tartışmanın süreceği toplam tur sayısı. Varsayılan 2'dir.

        Returns:
            Tüm turlarda üretilen `AgentMessage` nesnelerinin kronolojik listesi.
        """
        all_messages: list[AgentMessage] = []

        for round_num in range(1, rounds + 1):
            round_messages: list[AgentMessage] = []

            for agent in agents:
                all_prior: list[AgentMessage] = []
                
                # Önceki turlardaki mesajları ekle
                if all_messages:
                    all_prior.extend(all_messages)
                
                # Aynı turda kendisinden önceki ajanların mesajlarını ekle
                if round_messages:
                    all_prior.extend(round_messages)

                # Ajanın analizi
                raw_message = agent.analyze(
                    scenario_inputs=scenario,
                    previous_messages=all_prior if all_prior else None,
                )

                # Tur bilgisiyle mesajın yeniden oluşturularak kaydedilmesi
                message_with_round = AgentMessage(
                    agent=raw_message.agent,
                    stance=raw_message.stance,
                    confidence=raw_message.confidence,
                    reasoning=raw_message.reasoning,
                    metrics=raw_message.metrics,
                    round_number=round_num,
                )

                round_messages.append(message_with_round)

            # Bu turun mesajlarını genel listeye ekle
            all_messages.extend(round_messages)

        return all_messages
