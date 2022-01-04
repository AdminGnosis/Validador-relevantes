import os
from flask import Flask, request, render_template, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
from Validador_relevantes import relevantes
import pandas as pd


UPLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/uploads'
DOWNLOAD_FOLDER = os.path.dirname(os.path.abspath(__file__)) + '/downloads'

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER


@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    if request.method == 'POST':
        if request.files:
            f = request.files['archivo']
            filename = secure_filename(f.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            f.save(file_path)
            reporte = relevantes(file_path)
            #erroresf = reporte[0]
            #bitacoraf = reporte[1]
            writer = pd.ExcelWriter(app.config['DOWNLOAD_FOLDER']+'/' + 'errores.xlsx')
            file = 'errores.xlsx'
            reporte[0].to_excel(writer, sheet_name="Errores", index=False)
            reporte[1].to_excel(writer, sheet_name="Bitacora", index=False)
            writer.save()
            writer.close()
            file = 'errores.xlsx'
            return redirect(url_for('uploaded_file', filename=file))
    return render_template('index.html')


@app.route('/upload/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['DOWNLOAD_FOLDER'], filename, as_attachment=True)


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=4000, debug=True)
