"""Document encoding utilities."""

import base64
from pathlib import Path


def encode_document(document_path: str | Path) -> tuple[str, str]:
    """Read and base64-encode a document.

    Args:
        document_path: Path to the document file.

    Returns:
        Tuple of (base64_data, doc_type) where doc_type is ``"pdf"`` or ``"image"``.

    Raises:
        FileNotFoundError: If the document does not exist.
    """
    path = Path(document_path)
    if not path.exists():
        raise FileNotFoundError(f"Document not found: {document_path}")

    doc_bytes = path.read_bytes()
    doc_base64 = base64.b64encode(doc_bytes).decode("ascii")
    doc_type = "pdf" if doc_bytes.startswith(b"%PDF") else "image"

    return doc_base64, doc_type
