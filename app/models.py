"""Modelos de dados para vagas de estágio em Ciências Sociais (stdlib only)."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field


@dataclass
class JobPosting:
    """Esquema JSON de uma vaga de estágio."""

    titulo: str
    empresa: str
    link: str
    localidade: str
    descricao: str
    area_especifica: str
    requisitos: list[str] = field(default_factory=list)

    def to_dict(self) -> dict:
        return asdict(self)
