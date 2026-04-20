from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.domain.models import ScenarioInput, ScenarioRecord
from app.domain.repositories import ScenarioRepository
from app.infrastructure.database.models import ScenarioORM


class SqlAlchemyScenarioRepository(ScenarioRepository):
    def __init__(self, db: AsyncSession) -> None:
        self.db = db

    async def create(self, scenario: ScenarioInput) -> int:
        row = ScenarioORM(
            name=scenario.name,
            description=scenario.description,
            budget_million_usd=scenario.budget_million_usd,
            expected_roi_percent=scenario.expected_roi_percent,
            risk_level=scenario.risk_level,
            team_readiness=scenario.team_readiness,
        )
        self.db.add(row)
        await self.db.commit()
        await self.db.refresh(row)
        return row.id

    async def list(self, limit: int = 20, offset: int = 0) -> list[ScenarioRecord]:
        stmt = (
            select(ScenarioORM)
            .order_by(ScenarioORM.created_at.desc(), ScenarioORM.id.desc())
            .limit(limit)
            .offset(offset)
        )
        result = await self.db.execute(stmt)
        rows = result.scalars().all()
        return [self._to_domain(row) for row in rows]

    async def get_by_id(self, scenario_id: int) -> ScenarioRecord | None:
        row = await self.db.get(ScenarioORM, scenario_id)
        if row is None:
            return None
        return self._to_domain(row)

    @staticmethod
    def _to_domain(row: ScenarioORM) -> ScenarioRecord:
        return ScenarioRecord(
            id=row.id,
            name=row.name,
            description=row.description,
            budget_million_usd=row.budget_million_usd,
            expected_roi_percent=row.expected_roi_percent,
            risk_level=row.risk_level,
            team_readiness=row.team_readiness,
            created_at=row.created_at,
        )
