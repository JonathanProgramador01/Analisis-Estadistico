from bs4 import BeautifulSoup
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor
from reportlab.lib.utils import ImageReader
import plotly.io as pio

class Pdf():
    def __init__(self, prosesamiento):
        self.prosesamiento = prosesamiento
        self.c = canvas.Canvas("reporte.pdf", pagesize=letter)
        self.width, self.height = letter
        self.seguidor  = 0
        title = "Reporte de Análisis de Datos"
        
        self.c.setFont("Helvetica-Bold", 40)
        self.c.setFillColor(HexColor("#3D3D3D")) 
        self.c.drawString(30, self.height - 50, title)
        
        self.c.setLineWidth(1)
        # Ajustar la longitud de la línea para que coincida con el ancho del texto
        self.c.line(30, self.height - 53, 30 + self.c.stringWidth(title, "Helvetica-Bold", 40), self.height - 53)
                

    
    def descripcion_general(self, filename):
        #Titulo de la sección
        self.c.setFont("Helvetica-Oblique", 25)
        self.c.setFillColor(HexColor("#0F4761"))

        self.c.drawString(40, self.height - 120, "Descripción General")


        #Biene el nombre del subtitulo y despues de nuestro texto
        
        self.c.setFont("Helvetica", 18)
        self.c.setFillColor(HexColor("#0F4761")) 
        
        self.c.drawString(40, self.height - 160, "Nombre del Archivo")
        
        self.c.setFillColor(HexColor("#000000")) 
        self.c.setFont("Helvetica", 14)
        self.c.drawString(40, self.height - 180, filename)




        self.c.setFont("Helvetica", 18)
        self.c.setFillColor(HexColor("#0F4761")) 
        self.c.drawString(40, self.height - 210, "Shape")

        self.c.setFont("Helvetica", 14)
        self.c.setFillColor(HexColor("#000000")) 
        text = self.c.beginText(40, self.height - 230)
        text.textLines(f"Filas: {self.prosesamiento.data.shape[0]}\nColumnas: {self.prosesamiento.data.shape[1]}")
        self.c.drawText(text)
                
        
        self.c.setFillColor(HexColor("#0F4761")) 
        self.c.setFont("Helvetica", 18)
        self.c.drawString(40, self.height - 280, "NaN or Duplicados")    
        
        self.c.setFillColor(HexColor("#000000")) 
        self.c.setFont("Helvetica", 14)
        text = self.c.beginText(40, self.height - 300)
        text.textLines(f"Nan Valores: {self.prosesamiento.get_nan()[0]}\nTotal NAN: {self.prosesamiento.get_nan()[1]}"
                       f"\n Duplicados Valores (Fila): {self.prosesamiento.get_duplicates()[0]}\nTotal Duplicados: {self.prosesamiento.get_duplicates()[1]}")
        self.c.drawText(text)
        
        
        
        self.c.setFillColor(HexColor("#0F4761"))
        self.c.setFont("Helvetica", 18)
        self.c.drawString(40, self.height - 390, "Columnas")
        self.seguidor = 410
        
        self.c.setFont("Helvetica", 14)
        self.c.setFillColor(HexColor("#000000")) 
        for idx,column in enumerate(self.prosesamiento.get_columns_all()):
            

            text = self.c.beginText(40, self.height - ((410+(idx*20))))
            text.textLines(f"{column[0]}: '{column[1]}' (Nan: {column[2]}, Duplicados: {column[3]})")
            self.c.drawText(text)
        
            
    def estadisticas_basicas(self):
        self.c.showPage()
        self.c.setFont("Helvetica-Oblique", 25)
        self.c.setFillColor(HexColor("#0F4761")) 
        self.c.drawString(40, self.height - 70  , "Estadísticas Básicas")
        
        
        
        heading2 = 110
        parrafo = 130
        for idx,estadisticas in enumerate(self.prosesamiento.get_describe_statistics()):
            
            self.c.setFont("Helvetica", 18)
            self.c.setFillColor(HexColor("#0F4761")) 
            self.c.drawString(40, self.height - heading2, f"{estadisticas[0]}")
            
            self.c.setFont("Helvetica", 14)
            self.c.setFillColor(HexColor("#000000"))
            
            
    
            text = self.c.beginText(40, self.height-parrafo)
            text.textLines(f"Count: {estadisticas[0]}\n"
                           f"Media: {estadisticas[1]}\n"
                           f"Mediana: {estadisticas[2]}\n"
                           f"Moda: {estadisticas[3]}\n"
                           f"Desviación Estándar: {estadisticas[4]}\n"
                           f"Varianza: {estadisticas[5]}\n"
                           f"Mínimo: {estadisticas[6]}\n"
                           f"Máximo: {estadisticas[7]}\n"
                           f"Percentil 25: {estadisticas[8]}\n"
                           f"Percentil 50: {estadisticas[9]}\n"
                           f"Percentil 75: {estadisticas[10]}\n")
                           
            self.c.drawText(text)
            heading2 +=230
            parrafo += 230
            
            
            if heading2 > 800 or parrafo > 800:
                self.c.showPage()
                heading2 = 70
                parrafo = 90
            



    def estadisticas_inferencial(self):
        
        self.c.showPage()
        self.c.setFont("Helvetica-Oblique", 25)
        self.c.setFillColor(HexColor("#0F4761")) 
        self.c.drawString(40, self.height - 70  , "Estadísticas Inferenciales")
        
        heading2 = 110
        parrafo = 130
        for idx,estadisticas in enumerate(self.prosesamiento.get_statisticas_inferencial()):
            
            self.c.setFont("Helvetica", 18)
            self.c.setFillColor(HexColor("#0F4761")) 
            self.c.drawString(40, self.height - heading2, f"{estadisticas[0]}")
            
            self.c.setFont("Helvetica", 14)
            self.c.setFillColor(HexColor("#000000"))
            
            
    
            text = self.c.beginText(40, self.height-parrafo)
            text.textLines(f"Media: {estadisticas[1]}\n"
                           f"Media Muestra: {estadisticas[2]}\n"
                           f"Desviación Estándar: {estadisticas[3]}\n"
                           f"Desviación Estándar Muestra: {estadisticas[4]}\n"
                           f"Intervalo de Confianza: {estadisticas[5]}\n")
                           
            self.c.drawText(text)
            heading2 +=130
            parrafo += 130
            
            
            if heading2 > 800 or parrafo > 800:
                self.c.showPage()
                heading2 = 70
                parrafo = 90
        
        


    def histogramas(self):
        self.c.showPage()        
        self.c.setFont("Helvetica-Oblique", 25)
        self.c.setFillColor(HexColor("#0F4761")) 
        self.c.drawString(40, self.height - 70  , "Histogramas")

        for img_file in self.prosesamiento.histograma_images():
            # Verificar dimensiones de la imagen
            img = ImageReader(img_file)
            img_width, img_height = img.getSize()
            
            # Escalar la imagen para ajustarla al tamaño de la página
            aspect_ratio = img_width / img_height
            if img_width > self.width or img_height > self.height:
                if aspect_ratio > 1:
                    # Imagen más ancha que alta
                    new_width = self.width - 50  # Deja un margen
                    new_height = new_width / aspect_ratio
                else:
                    # Imagen más alta que ancha
                    new_height = self.height - 50
                    new_width = new_height * aspect_ratio
            else:
                # Si la imagen ya cabe en la página
                new_width, new_height = img_width, img_height
            
            # Centrar la imagen en la página
            x = (self.width - new_width) / 2
            y = (self.height - new_height) / 2
            
            # Dibujar la imagen en la página
            self.c.drawImage(img_file, x, y, width=new_width, height=new_height)
            
            # Agregar nueva página para la siguiente imagen
            self.c.showPage()
        
    
            
    def save(self):
        self.c.save()








# c.setFont("Helvetica", 14)
# c.drawString(80, height - 120, "Nombre del Archivo")
# c.drawString(80, height - 140, file)




