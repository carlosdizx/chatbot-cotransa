import re
from typing import Optional


def extract_tracking_number(text: str) -> Optional[str]:
    """
    Extrae un número de seguimiento del texto proporcionado.

    Se asume que el número de seguimiento es una secuencia alfanumérica de al menos 5 caracteres.
    La función primero busca patrones asociados a frases comunes como "número de seguimiento" o "tracking number".
    Si no lo encuentra, intenta obtener la primera secuencia alfanumérica suficientemente larga.

    :param text: Entrada del usuario.
    :return: El número de seguimiento extraído o None si no se encuentra.
    """
    # Buscar patrones del tipo "número de seguimiento: XYZ123" o "tracking number XYZ123"
    pattern = r"(?:número de seguimiento|tracking number)[^\w]*([\w\d]{5,})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        return match.group(1)

    # Si no se encuentra ese patrón, se intenta obtener cualquier secuencia alfanumérica de 5 o más caracteres
    match = re.search(r"\b[\w\d]{5,}\b", text)
    if match:
        return match.group(0)

    return None
