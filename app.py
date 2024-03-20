from flask import Flask, request, send_file
import PyPDF2
from reportlab.pdfgen import canvas
import io

app = Flask(__name__)

# Liste de mots-clés pour le calcul du score
KEYWORDS = ['python', 'data', 'machine learning']

@app.route('/upload', methods=['POST'])
def upload_file():
    uploaded_file = request.files['file']
    if uploaded_file.filename != '':
        # Lecture et analyse du CV
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + " "
        
        # Extraction des informations et calcul du score
        score = sum(text.count(keyword) for keyword in KEYWORDS)
        info = "Nom: ?, Prénom: ?, École: ?, Email: ?, Téléphone: ?, Score: " + str(score)

        # Génération du rapport PDF
        buffer = io.BytesIO()
        p = canvas.Canvas(buffer)
        p.drawString(100, 800, info)
        p.save()
        buffer.seek(0)
        
        return send_file(buffer, as_attachment=True, attachment_filename='rapport.pdf', mimetype='application/pdf')

    return "Aucun fichier envoyé", 400

if __name__ == '__main__':
    app.run(debug=True)