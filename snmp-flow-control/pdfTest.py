import pdfkit
import jinja2
import os

templateLoader = jinja2.FileSystemLoader(searchpath = './')
templateEnv = jinja2.Environment(loader = templateLoader)
TEMPLATE_FILE = 'reportTemplate.html'
template = templateEnv.get_template(TEMPLATE_FILE)
outputText = template.render(imageFile = os.path.abspath('traficoRED.png'))
print(outputText)
pdfkit.from_string(outputText, 'out1.pdf')

