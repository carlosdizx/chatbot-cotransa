from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas


def create_pdf(filename):
    page_width, page_height = A4
    c = canvas.Canvas(filename, pagesize=A4)

    c.setFont("Helvetica-Bold", 18)
    c.drawCentredString(page_width / 2, page_height - 80, "Guía de Envío Internacional")

    c.setFont("Helvetica", 12)
    lines = [
        "Número de Guía: PBEM054159",
        "Remitente: Logística Global S.A.",
        "Dirección Remitente: Calle Falsa 123, Ciudad, País",
        "",
        "Destinatario: Juan Pérez",
        "Dirección Destinatario: Avenida Siempre Viva 456, Ciudad, País",
        "",
        "Fecha de Envío: 10/02/2025",
        "",
        "Observaciones:",
        "  - Envío sujeto a control de aduanas.",
        "  - Manejar con cuidado."
    ]

    x = 50
    y = page_height - 130

    for line in lines:
        c.drawString(x, y, line)
        y -= 20

    c.showPage()
    c.save()
    print(f"The PDF '{filename}' has been generated successfully.")


if __name__ == "__main__":
    create_pdf("guia_envio_internacional.pdf")
