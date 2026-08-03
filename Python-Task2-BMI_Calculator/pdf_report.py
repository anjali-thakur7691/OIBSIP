from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus import Table
from reportlab.platypus import TableStyle
from reportlab.lib import colors


class PDFReport:

    def generate(self, records):

        pdf = SimpleDocTemplate("BMI_Report.pdf")

        data = [
            [
                "ID",
                "Name",
                "Age",
                "Gender",
                "Weight",
                "Height",
                "BMI",
                "Category",
                "Date"
            ]
        ]


            # ---------------------------------
        # Add Database Records
        # ---------------------------------

        for row in records:
            data.append(list(row))

        # ---------------------------------
        # Create Table
        # ---------------------------------

        table = Table(data)

        table.setStyle(TableStyle([

            ('BACKGROUND', (0, 0), (-1, 0), colors.darkblue),

            ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),

            ('GRID', (0, 0), (-1, -1), 1, colors.black),

            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),

            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),

            ('BOTTOMPADDING', (0, 0), (-1, 0), 10),

            ('ALIGN', (0, 0), (-1, -1), 'CENTER')

        ]))


        # ---------------------------------
        # Build PDF
        # ---------------------------------

        elements = []

        elements.append(table)

        pdf.build(elements)

        return "BMI_Report.pdf"