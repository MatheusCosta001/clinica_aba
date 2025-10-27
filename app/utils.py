from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

def gerar_relatorio_pdf(paciente, evolucoes, gerador_nome='Sistema'):
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    styles = getSampleStyleSheet()
    story = []

    story.append(Paragraph(f'Ficha do Paciente: {paciente.nome}', styles['Title']))
    story.append(Spacer(1, 12))
    story.append(Paragraph(f'Data de Nascimento: {paciente.data_nascimento}', styles['Normal']))
    story.append(Paragraph(f'Diagnóstico: {paciente.diagnostico or "-"}', styles['Normal']))
    story.append(Paragraph(f'Responsável: {paciente.responsavel or "-"}', styles['Normal']))
    story.append(Spacer(1, 12))

    story.append(Paragraph('Evoluções:', styles['Heading2']))
    for e in evolucoes:
        autor = e.autor.nome if hasattr(e, 'autor') and e.autor else f'Usuário {e.usuario_id}'
        texto = f"{e.data_hora.strftime('%Y-%m-%d %H:%M')} - {autor}: {e.anotacao}"
        story.append(Paragraph(texto, styles['Normal']))
        story.append(Spacer(1, 6))

    story.append(Spacer(1, 12))
    story.append(Paragraph(f'Relatório gerado por: {gerador_nome}', styles['Normal']))

    doc.build(story)
    buffer.seek(0)
    return buffer
