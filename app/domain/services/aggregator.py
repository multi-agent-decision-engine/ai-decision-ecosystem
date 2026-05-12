from app.domain.models import AgentMessage, AggregatedDecision, FinalDecision


class DecisionAggregator:
    """
    Ajan mesajlarını (AgentMessage) nihai bir öneri halinde birleştirir.

    Eşit ağırlıklı ortalama ve senaryo tipi sınıflandırmasına dayalı
    ağırlıklı toplama işlemlerini destekler.
    """

    def aggregate(
        self,
        messages: list[AgentMessage],
        weights: dict[str, float] | None = None,
    ) -> AggregatedDecision:
        """
        Ajan mesajlarını nihai karara dönüştürür.

        Skor hesaplaması:
        - support -> confidence * 100
        - oppose -> (1 - confidence) * 100
        - neutral -> 50

        Args:
            messages: Ajan analiz sonuçlarının listesi.
            weights: İsteğe bağlı ajan_adı → ağırlık (0-1) sözlüğü.
                     None ise eşit ağırlık kullanılır.
                     Ağırlıkların toplamı 1.0 olmalıdır.

        Returns:
            Nihai skor ve kararı içeren AggregatedDecision.
        """
        if not messages:
            raise ValueError("messages boş olamaz")

        total_weight = 0.0
        weighted_sum = 0.0

        if weights:
            for message in messages:
                # Skor hesaplaması
                if message.stance == "support":
                    score = message.confidence * 100
                elif message.stance == "oppose":
                    score = (1 - message.confidence) * 100
                else:  # neutral
                    score = 50.0

                agent_weight = weights.get(message.agent, 1.0 / len(messages))
                weighted_sum += score * agent_weight
                total_weight += agent_weight

            # Ortalama hesabı: ağırlıklar 1'e toplanmıyorsa normalize et
            average = weighted_sum / total_weight if total_weight > 0 else 0
        else:
            for message in messages:
                if message.stance == "support":
                    score = message.confidence * 100
                elif message.stance == "oppose":
                    score = (1 - message.confidence) * 100
                else:  # neutral
                    score = 50.0
                weighted_sum += score
            average = weighted_sum / len(messages)

        if average >= 75:
            decision = FinalDecision.APPROVE
        elif average >= 50:
            decision = FinalDecision.REVISE
        else:
            decision = FinalDecision.REJECT

        return AggregatedDecision(final_score=round(average, 2), decision=decision)
