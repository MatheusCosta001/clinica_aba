from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO
from datetime import datetime

def gerar_relatorio_pdf(paciente, evolucoes, gerador_nome):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, f"Relatório do paciente: {paciente.nome}")
    y -= 20
    c.setFont("Helvetica", 10)
    c.drawString(40, y, f"Gerado por: {gerador_nome}  —  Data: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    y -= 30

    # Dados do paciente
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Dados do paciente:")
    y -= 18
    c.setFont("Helvetica", 10)
    linhas = [
        f"Nome: {paciente.nome}",
        f"Data Nasc.: {paciente.data_nascimento or ''}",
        f"Idade: {paciente.idade or ''}",
        f"Diagnóstico: {paciente.diagnostico or ''}",
        f"Responsável: {paciente.responsavel or ''}",
        f"Endereço: {paciente.rua or ''} - {paciente.bairro or ''} - {paciente.cidade or ''}/{paciente.uf or ''} - CEP: {paciente.cep or ''}"
    ]
    for L in linhas:
        c.drawString(50, y, L)
        y -= 14

    y -= 10
    c.setFont("Helvetica-Bold", 12)
    c.drawString(40, y, "Evoluções selecionadas:")
    y -= 18
    c.setFont("Helvetica", 10)

    for e in evolucoes:
        texto = f"{e.data_hora.strftime('%Y-%m-%d %H:%M')} — {e.usuario.nome} ({e.area or ''}): {e.anotacao}"
        # quebra simples de linha
        for i in range(0, len(texto), 110):
            if y < 60:
                c.showPage()
                y = height - 50
            c.drawString(50, y, texto[i:i+110])
            y -= 14
        y -= 6

    c.showPage()
    c.save()
    buffer.seek(0)
    return buffer
