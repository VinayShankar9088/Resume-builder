from flask import Flask, render_template, request, redirect, url_for, flash, make_response
from werkzeug.utils import secure_filename
import pdfkit
import os
from pathlib import Path

# -------------------- Setup --------------------
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_FOLDER = BASE_DIR / 'static' / 'uploads'
UPLOAD_FOLDER.mkdir(parents=True, exist_ok=True)
ALLOWED_EXT = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.secret_key = 'change-me-to-a-secure-key'
app.config['UPLOAD_FOLDER'] = str(UPLOAD_FOLDER)
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024  # 2MB

# -------------------- Helper --------------------
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXT

def get_form_data():
    return {
        "name": request.form.get("name", "").strip(),
        "email": request.form.get("email", "").strip(),
        "phone": request.form.get("phone", "").strip(),
        "summary": request.form.get("summary", "").strip(),
        "skills": [s.strip() for s in request.form.get("skills", "").split("\n") if s.strip()],
        "educations": [e.strip() for e in request.form.get("education", "").split("\n") if e.strip()],
        "projects": [p.strip() for p in request.form.get("projects", "").split("\n") if p.strip()],
        "experiences": [ex.strip() for ex in request.form.get("experience", "").split("\n") if ex.strip()],
        "certificates": [c.strip() for c in request.form.get("certificates", "").split("\n") if c.strip()],
    }

# -------------------- Routes --------------------
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    data = get_form_data()
    template_choice = request.form.get('template', 'template1')

    if not data["name"]:
        flash("Name is required.")
        return redirect(url_for("index"))

    # Photo upload
    photo_filename = None
    if 'photo' in request.files:
        photo = request.files['photo']
        if photo and photo.filename != '' and allowed_file(photo.filename):
            filename = secure_filename(photo.filename)
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            photo.save(save_path)
            photo_filename = f'uploads/{filename}'

    data["photo"] = photo_filename
    data["template_choice"] = template_choice

    # PDF download option
    if request.form.get("download") == "pdf":
        html = render_template(f"{template_choice}.html", **data)

        # Save HTML for debugging
        with open("debug.html", "w", encoding="utf-8") as f:
            f.write(html)

        # PDFKit configuration
        config = pdfkit.configuration(wkhtmltopdf=r'C:\\Program Files\\wkhtmltopdf\\bin\\wkhtmltopdf.exe')
        options = {
            'enable-local-file-access': None,
            'page-size': 'A4',
            'encoding': 'UTF-8',
            'quiet': ''
        }

        try:
            output_path = os.path.join(BASE_DIR, "resume.pdf")
            pdfkit.from_string(html, output_path, configuration=config, options=options)

            # Serve the file as download
            with open(output_path, "rb") as f:
                pdf_data = f.read()

            response = make_response(pdf_data)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = 'attachment; filename=resume.pdf'
            return response

        except Exception as e:
            flash(f"PDF generation failed: {e}")
            return redirect(url_for("index"))

    return render_template(f"{template_choice}.html", **data)

# -------------------- Run App --------------------
if __name__ == "__main__":
    app.run(debug=True)