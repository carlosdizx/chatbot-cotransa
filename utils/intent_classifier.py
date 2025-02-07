import re


def classify_intent(user_input: str) -> str:
    user_input = user_input.lower()

    if re.search(r"(dónde está mi paquete|estado de mi pedido|seguimiento|track)", user_input):
        return "envios"

    elif re.search(r"(aduana|retención|trámite aduanero|despacho aduanal)", user_input):
        return "aduanas"

    elif re.search(r"(producto|artículo|detalles del producto|información del producto)", user_input):
        return "productos"

    else:
        return "desconocido"
