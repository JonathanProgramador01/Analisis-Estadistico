import os
import tempfile

from flask import Flask, render_template, request, flash, current_app, url_for, redirect
from flask_wtf import FlaskForm
from flask import Flask
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from werkzeug.utils import secure_filename
from procesamiento import Prosesamiento
from pdf import Pdf



app = Flask(__name__)

app.secret_key = "supersecretakey"
app.config["UPLOAD_EXTENSIONS"] = [".csv"]


@app.route("/", methods = ["GET", "POST"])
def upload():
    global prosesamiento, filename 
    
    if request.method == "POST":
        file = request.files['file']

        if file.filename == "":
            flash("Porfavor seleccione un archivo")

        else:
            filename = secure_filename(file.filename)
            file_ext = os.path.splitext(filename)[1]
            if file_ext not in current_app.config["UPLOAD_EXTENSIONS"]:
                flash("Unicamente se aceptan .csv")
            else:
                with tempfile.TemporaryDirectory() as temp_dir:
                    file_path = os.path.join(temp_dir, filename)
                    file.save(file_path)  # Guardar el archivo en el directorio temporal
                    prosesamiento = Prosesamiento(file_path)
                    
                    
                    return redirect(url_for("descripcion_general"))

    return render_template("upload.html" )




@app.route("/descripcion_general")
def descripcion_general():

    return render_template("dashboard/descripcion_general.html",prosesamiento=prosesamiento, filename=filename)


@app.route("/estadisticas_basicas")
def estadisticas_basicas():
    return  render_template("dashboard/estadisticas_basicas.html", prosesamiento=prosesamiento)


@app.route("/estadisticas_inferencial")
def estadisticas_inferencial():
    return  render_template("dashboard/estadisticas_inferencial.html", prosesamiento=prosesamiento)


@app.route("/histogramas")
def histogramas():
    return render_template("dashboard/histogramas.html", prosesamiento=prosesamiento)


@app.route("/diagramas_de_cajas")
def diagramas_de_cajas():
    return render_template("dashboard/diagramas_de_cajas.html", prosesamiento=prosesamiento)


@app.route("/graficos_de_dispersion")
def graficos_de_dispersion():
    return render_template("dashboard/graficos_de_dispersion.html", prosesamiento=prosesamiento)


@app.route("/exportar")
def exportar():
    
    pdf = Pdf(prosesamiento)
    pdf.descripcion_general(filename) 
    pdf.estadisticas_basicas()
    pdf.estadisticas_inferencial()
    pdf.histogramas()
    pdf.save()
     
    return render_template("dashboard/exportar.html")





    
    
    
    
    
    


if __name__ == "__main__":
    app.run(debug=True)