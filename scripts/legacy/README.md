# scripts/legacy/

Scripts one-shot mantidos por valor histórico. **Não fazem parte da arquitetura suportada.**

| Script | Origem | Por que está aqui |
|---|---|---|
| `clean_markdown_for_tsx.py` | sessão ad-hoc, abr/2026 | Limpava `#`, `**`, `---` em strings de TSX já gerado. Substituído pelo `parse_module_to_sections` no parser canônico. |
| `convert_drafts_to_tsx.py` | sessão ad-hoc, abr/2026 | Hoje é o subcomando `python cli.py drafts-to-tsx` (`src/converters/draft_to_course.py`). |
| `generate_joias_course.py` | sessão ad-hoc, abr/2026 | Geração one-shot do curso de joias, usava paths hardcoded. Hoje use o pipeline normal com cliente customizado. |
| `generate_joias_course_v2.py` | sessão ad-hoc, abr/2026 | Iteração sobre o anterior. |

Se precisar usar algo daqui, leia primeiro — todos têm caminhos absolutos e suposições obsoletas.
