from datetime import date, datetime
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageBreak, Paragraph, Spacer


class BancaryReportFacade:

    __instance = None
    __ancho_pagina = 841.89
    __alto_pagina = 595.27  

    def __BancaryReportFacade(self):
        #Constructor privado
        pass

    def __new__(cls):
        if not cls.__instance:
            cls.__instance = super(BancaryReportFacade, cls).__new__(cls)
            print("No existe")
        else:
            print("Ya existe")

        return cls.__instance
    


    def generatePDF(cls, response, nombreDistribuidor, info:list):
        pdf = SimpleDocTemplate(response, pagesize=landscape(A4))

        elements = []

        def draw_header(canvas, doc):
            canvas.saveState()
            canvas.setFillColorRGB(221/255,238/255,239/255)
            canvas.rect(0,0,cls.__ancho_pagina,cls.__alto_pagina,fill=1)
            canvas.setFillColorRGB(0,0,0)
            canvas.setFont('Helvetica', 12)
            canvas.drawString(cls.__ancho_pagina - 80, cls.__alto_pagina - 20, date.today().strftime("%d/%m/%Y"))
            canvas.drawString(cls.__ancho_pagina - 80, cls.__alto_pagina - 40, datetime.now().strftime("%H:%M:%S"))
            canvas.drawInlineImage("\chibchaweb_django\static\images\logo.jpg", 390-cls.__ancho_pagina, cls.__alto_pagina - 60, preserveAspectRatio=True, height=50)
            canvas.drawString(90, cls.__alto_pagina - 40, 'CibchaWeb')
            canvas.drawCentredString(cls.__ancho_pagina / 2, cls.__alto_pagina - 85, "Reporte Bancario " + nombreDistribuidor)
            canvas.restoreState()

        pdf.build(elements, onFirstPage=draw_header, onLaterPages=draw_header)

        #Agregar tabla
        data = [['Nombre dominio', 'Extensión dominio', 'Nombre Cliente',  'Fecha Registro' , 'Valor Total Contrato', 'Valor Comisión', 'Tarjeta de Crédito'],]
        data.extend(info[:-3])
        ancho_columna = (cls.__ancho_pagina * 4.5 / 5) / len(data[0])
        ancho_columnas = [ancho_columna] * len(data[0])
        table = Table(data, colWidths=ancho_columnas, spaceBefore=20, spaceAfter=20)

        style = TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.Color(38/255, 239/255, 250/255)), 
        ('LINEABOVE', (0,1), (-1,-1), 1, colors.black),
        ('LINEBELOW', (0,-1), (-1,-1), 1, colors.black),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),  
        ('BOX', (0,0), (-1,-1), 1, colors.black),
        ])

        for i in range(1, len(data)):
            if i % 2 == 0:
                bg_color = colors.white
            else:
                bg_color = colors.Color(186/255, 199/255, 199/255)
            style.add('BACKGROUND', (0, i), (-1, i), bg_color)

        table.setStyle(style)

        elements.append(Spacer(1, 10))  # Add a spacer before the table
        elements.append(table)
        elements.append(PageBreak())

        print(info)

        elements.append(Paragraph("Total mensual: COP " + info[-3]))
        elements.append(Paragraph("Total comisión a ChibchaWeb: COP " + info[-2]))
        elements.append(Paragraph("Total ingresos mensuales: COP " + info[-1])) 

        pdf.build(elements)
