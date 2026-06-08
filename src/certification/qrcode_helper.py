"""Helper para geração de QR code em base64.

Gera PNG de QR code embutido como data URI, permitindo certificados
HTML totalmente autossuficientes (sem dependências externas em tempo
de visualização).

Dependência externa::

    pip install qrcode[pil]>=7.4

A biblioteca ``qrcode`` (com Pillow) é opcional. Quando ausente, a
função levanta ``RuntimeError`` claramente — o código de teste deve
usar mock ou ``pytest.importorskip("qrcode")``.

Não modificamos ``pyproject.toml`` neste quickwin (Wave 9 V0). A
recomendação é adicionar ``qrcode[pil]>=7.4`` como dependência
opcional ``[project.optional-dependencies] certification`` quando
sair de V0.
"""

from __future__ import annotations

import base64
import io


def qr_to_base64_png(url: str, size: int = 200) -> str:
    """Gera QR code PNG codificado em base64 a partir de uma URL.

    Args:
        url: URL pública para verificação do certificado.
        size: Tamanho lateral aproximado em pixels (controla box_size).

    Returns:
        String base64 (sem prefixo ``data:image/png;base64,``) pronta
        para embutir em ``<img src="data:image/png;base64,..."/>``.

    Raises:
        RuntimeError: se a lib ``qrcode`` não estiver instalada.
        ValueError: se URL vazia.
    """
    if not url or not url.strip():
        raise ValueError("URL não pode ser vazia para gerar QR code")

    try:
        import qrcode  # type: ignore[import-not-found]
    except ImportError as exc:  # pragma: no cover - depende do ambiente
        raise RuntimeError(
            "Biblioteca 'qrcode' não está instalada. "
            "Instale com: pip install qrcode[pil]>=7.4"
        ) from exc

    # Calcula box_size a partir do tamanho desejado.
    # Versão 1 do QR padrão = 21 módulos; com border 4 default => 29 módulos.
    box_size = max(1, size // 29)

    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=4,
    )
    qr.add_data(url)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    buffer = io.BytesIO()
    img.save(buffer, format="PNG")
    return base64.b64encode(buffer.getvalue()).decode("ascii")
