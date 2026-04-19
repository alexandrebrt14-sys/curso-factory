"""Multi-tenancy do curso-factory.

ClientContext encapsula tudo que varia entre clientes: autor, domínio, voice
guard rules, padrão editorial, integração com landing page, diretórios de
output. Agentes, validadores e geradores recebem ClientContext em vez de
consultar constantes globais hardcoded.

Uso típico:
    from src.clients import load_client
    client = load_client("default")  # ou "minha_empresa"
"""

from src.clients.context import (
    Author,
    Branding,
    ClientContext,
    Company,
    Domain,
    Editorial,
    VoiceGuardCanonical,
    VoiceGuardConfig,
    VoiceGuardForbidden,
)
from src.clients.loader import get_client_from_env, list_clients, load_client

__all__ = [
    "Author",
    "Branding",
    "ClientContext",
    "Company",
    "Domain",
    "Editorial",
    "VoiceGuardCanonical",
    "VoiceGuardConfig",
    "VoiceGuardForbidden",
    "get_client_from_env",
    "list_clients",
    "load_client",
]
