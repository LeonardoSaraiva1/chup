"""Fontes de vagas (MVP com base curada local + filtro por localidade)."""

from __future__ import annotations

from app.filtering import classify_area, is_social_science_job
from app.models import JobPosting

CURATED_JOBS = [
    {
        "titulo": "Estágio em Pesquisa de Opinião Pública",
        "empresa": "Instituto Vox Cidadã",
        "link": "https://example.org/vagas/vox-estagio-opiniao",
        "localidade": "São Paulo, SP",
        "descricao": "Apoio em survey, tabulação de dados, análise quantitativa e relatórios de opinião pública.",
        "requisitos": ["Excel/Sheets", "Interesse em Ciência Política", "Leitura de indicadores sociais"],
    },
    {
        "titulo": "Estágio em Antropologia Urbana",
        "empresa": "ONG Territórios Vivos",
        "link": "https://example.org/vagas/ong-antropologia-urbana",
        "localidade": "Recife, PE",
        "descricao": "Pesquisa qualitativa com entrevistas de campo e produção de notas etnográficas.",
        "requisitos": ["Condução de entrevistas", "Escrita analítica", "Disponibilidade para campo"],
    },
    {
        "titulo": "Estágio em Avaliação de Políticas Públicas",
        "empresa": "Fundação Observa Brasil",
        "link": "https://example.org/vagas/fundacao-politicas-publicas",
        "localidade": "Brasília, DF",
        "descricao": "Suporte na avaliação de programas sociais, monitoramento de indicadores e revisão bibliográfica.",
        "requisitos": ["Leitura acadêmica", "Noções de metodologia", "Interesse por gestão pública"],
    },
    {
        "titulo": "Estágio de Recursos Humanos Generalista",
        "empresa": "Empresa XPTO",
        "link": "https://example.org/vagas/rh-generalista",
        "localidade": "São Paulo, SP",
        "descricao": "Apoio ao recrutamento, seleção e benefícios do time corporativo.",
        "requisitos": ["Pacote Office"],
    },
]


def fetch_jobs(localidade: str | None = None) -> list[JobPosting]:
    """Retorna vagas filtradas por aderência temática e localidade."""

    normalized_local = (localidade or "").strip().lower()
    results: list[JobPosting] = []

    for raw in CURATED_JOBS:
        if not is_social_science_job(raw["titulo"], raw["descricao"]):
            continue

        if normalized_local and normalized_local not in raw["localidade"].lower():
            continue

        area = classify_area(f"{raw['titulo']} {raw['descricao']}")
        results.append(
            JobPosting(
                titulo=raw["titulo"],
                empresa=raw["empresa"],
                link=raw["link"],
                localidade=raw["localidade"],
                descricao=raw["descricao"],
                area_especifica=area,
                requisitos=raw.get("requisitos", []),
            )
        )

    return results
