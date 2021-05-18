DEBUG = False

# Miscellaneous
from io import StringIO
import random
import re
import alumno

# Process CSV files
import csv

# Generate PDFs using ReportLab
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Table
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import LETTER
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch, mm
from reportlab.graphics.barcode import code39

PAGE_HEIGHT= 11 * inch
PAGE_WIDTH= 8.5 * inch
styles = getSampleStyleSheet()
Title = "Pago de inscripción"

def process_data(datos):
    ''' Process a csv file containing lastname and firstname.
    Return a list of lists containing lastname, firstname, and random identifier
    '''
    choices = range(100000)
    newdata = [datos[0],datos[1],datos[0][:3].upper() +'-'+str(random.choice(choices))]
    
    return newdata

def docPage(canvas, doc):
    canvas.saveState()
    canvas.setFont('Times-Bold', 10)
    canvas.drawCentredString(PAGE_WIDTH/2.0, PAGE_HEIGHT - (.25 * inch), Title)
    canvas.setFont('Times-Roman',9)
    canvas.drawString(7 * inch, .75 * inch, "Page %d" % (doc.page,))
    canvas.restoreState()

def ticketPage(canvas, doc ):
    canvas.saveState()
    H = 1.5 * inch
    W = 1.5 * inch
    canvas.drawImage('itnl.png', 6 * inch, PAGE_HEIGHT - (1.75 * inch), width = W, height = H)
    canvas.restoreState()


def gen_ticket(row,fn):
    doc = SimpleDocTemplate(fn)
    Story = []
    styleN = styles["Normal"]
    styleH = styles['Heading1']
    Story.append(Paragraph("TECNM Campus Nuevo Laredo",styleH))
    Story.append(Paragraph("Comprobante de Pago",styleH))
    Story.append(Spacer(1 * inch, .5 * inch))
    Story.append(Paragraph("Número de control: %s" % (row[1]), styleN))
    Story.append(Paragraph("Alumno: %s %s" % (row[2], row[3]), styleN))
    Story.append(Paragraph("Carrera: %s" % (row[4]), styleN))
    Story.append(Paragraph("Monto pagado: $%s" % (row[6] - row[5]), styleN))
    Story.append(Paragraph("Monto restante: $%s" % (row[5]), styleN))
    Story.append(Paragraph("Pagado por: %s" % (row[7]), styleN))
    Story.append(Spacer(1 * inch, .25 * inch))
    Story.append(Paragraph("Estado: %s" % (row[8]), styleN))
    Story.append(Spacer(1 * inch, .25 * inch))
    Story.append(Paragraph("Código del comprobante: %s" % (row[0]), styleN))
    Story.append(Spacer(1 * inch, .5 * inch))
    barcode=code39.Extended39(row[0], barWidth= 0.02 * inch, barHeight= .5 * inch)
    Story.append(barcode)
    doc.build(Story, onFirstPage=ticketPage, onLaterPages=ticketPage)
    return

# create an re to get rid of non-word chars for file names
pattern = re.compile('[W_]+')

def generarTicket(miAlumno):
    miAlumno.RellenarAlumno()
    miAlumno.noControl = str(miAlumno.noControl)
    adeudo = miAlumno.calcularAdeudo()

    estado = "PAGADO" if miAlumno.adeudo <= 0 else "SIN PAGAR"

    choices = range(100000)
    data = (miAlumno.noControl[:3] +'-'+str(random.choice(choices)), miAlumno.noControl, miAlumno.nombre, miAlumno.apellidos, miAlumno.carrera, miAlumno.adeudo, adeudo, miAlumno.email, estado)

    fname =  pattern.sub('-', data[1] + "-ticket").lower()
    fname += ".pdf"
    gen_ticket(data, fname)

    return fname
