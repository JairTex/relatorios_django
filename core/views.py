import io

from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, HttpResponse
from django.template.loader import render_to_string
from django.views.generic import View
from reportlab.pdfgen import canvas
from weasyprint import HTML

###



###

class IndexView(View):
    def get(self, request, *args, **kwargs):
        #cria um arquivo para receber dados e gerar PDF
        buffer = io.BytesIO()

        #cria o arquivo pdf
        pdf = canvas.Canvas(buffer)

        #insere 'coisas' no pdf
        pdf.drawString(100, 100, 'Teste de PDF')

        #Quando acabamos de inserir:
        pdf.showPage()
        pdf.save()

        # Retornamos o buffer para o inicio do arquivo
        buffer.seek(0)

        # Faz o download do arquivo pdf gerado
        #return FileResponse(buffer, as_attachment=True, filename='relatorio1.pdf')

        #Abre o Pdf direto do navegador
        return FileResponse(buffer, filename='relatorio1.pdf')

class Index2View(View):

    def get(self, request, *args, **kwargs):
        texto = ['Teste ocorrendo', 'Tudo está funcionando', 'Relatório bem sucedido!']

        html_string = render_to_string('relatorio.html', {'texto' : texto})

        html = HTML(string=html_string)
        html.write_pdf(target='/tmp/relatorio2.pdf')

        fs =FileSystemStorage('/tmp')

        with fs.open('relatorio2.pdf') as pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            #Faz o download
            #response['content-Disposition'] = 'attachment; filename="relatorio2.pdf"'
            
            #Abre no navegador
            response['content-Disposition'] = 'inline; filename="relatorio2.pdf"'
        return response
