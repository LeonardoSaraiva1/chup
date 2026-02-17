"""Camada de filtragem semântica/regex para separar vagas relevantes."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class FilterConfig:
    """Configuração de padrões positivos e negativos."""

    positive_patterns: tuple[str, ...] = (
        r"\bsociologia\b",
        r"\bci[eê]ncias?\s+sociais\b",
        r"\bantropologia\b",
        r"\bci[eê]ncia\s+pol[ií]tica\b",
        r"\bpesquisa\s+(qualitativa|quantitativa)\b",
        r"\bpol[ií]ticas?\s+p[uú]blicas\b",
        r"\ban[aá]lise\s+de\s+dados\s+sociais\b",
        r"\bopini[aã]o\s+p[uú]blica\b",
        r"\bimpacto\s+social\b",
        r"\bibge\b",
        r"\bipea\b",
    )
    negative_patterns: tuple[str, ...] = (
        r"\bservi[cç]o\s+social\b",
        r"\bassistente\s+social\b",
        r"\brecursos\s+humanos\b",
        r"\brh\b",
        r"\brecrutamento\b",
        r"\bfolha\s+de\s+pagamento\b",
        r"\bbenef[ií]cios\b",
    )


FILTER_CONFIG = FilterConfig()


def _normalize(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def relevance_score(text: str, config: FilterConfig = FILTER_CONFIG) -> int:
    """Pontua relevância do texto.

    +2 para cada padrão positivo encontrado.
    -3 para cada padrão negativo encontrado.
    """

    normalized = _normalize(text)
    positive_hits = sum(bool(re.search(pattern, normalized)) for pattern in config.positive_patterns)
    negative_hits = sum(bool(re.search(pattern, normalized)) for pattern in config.negative_patterns)
    return (positive_hits * 2) - (negative_hits * 3)


def classify_area(text: str) -> str:
    """Classifica a vaga em uma trilha de interesse."""

    normalized = _normalize(text)
    if re.search(r"\b(quantitativa|estat[ií]stica|microdados|survey|econometria)\b", normalized):
        return "Pesquisa Quantitativa"
    if re.search(r"\b(qualitativa|entrevista|etnografia|grupo focal|campo)\b", normalized):
        return "Pesquisa Qualitativa"
    if re.search(r"\b(pol[ií]ticas? p[uú]blicas|gest[aã]o p[uú]blica|avalia[cç][aã]o de programas)\b", normalized):
        return "Políticas Públicas"
    return "Pesquisa Qualitativa"


def is_social_science_job(title: str, description: str) -> bool:
    """Decide se a vaga pertence ao escopo de Ciências Sociais."""

    score = relevance_score(f"{title} {description}")
    return score > 0
