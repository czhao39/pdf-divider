#!/usr/bin/env python3

import base64
from io import BytesIO
import os
from flask import *
from werkzeug.utils import secure_filename
from wand.image import Image, Color

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uploads/")
print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__, static_url_path="")
app.secret_key = b"\xd9h\xf8\xd2-\x8c\xe6\xdc;\r\xd9\x10'[\x03;"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


divider_ys = None


def is_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("submit_pdf.html")


@app.route("/divider", methods=["POST"])
def divider():
    # Save PDF
    if "file" not in request.files:
        flash("No file uploaded.")
        return redirect(request.url)
    pdf_file = request.files["file"]
    if not pdf_file or pdf_file.filename == "":
        flash("No file selected.")
        return redirect(request.url)
    if not is_allowed_file(pdf_file.filename):
        flash("Invalid file. Must be a PDF.")
        return redirect(request.url)
    pdf_filename = secure_filename(pdf_file.filename)
    path_to_pdf = os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
    pdf_file.save(path_to_pdf)

    # Convert to and save PNG to stream
    png_stream = BytesIO()
    with Image(filename=path_to_pdf) as pdf_image:
        num_pages = len(pdf_image.sequence)
        with Image(width=pdf_image.width, height=pdf_image.height * num_pages) as png_image:
            for p in range(num_pages):
                png_image.composite(
                    pdf_image.sequence[p],
                    top=pdf_image.height * p,
                    left=0
                )
                png_image.format = "png"
            png_image.background_color = Color("white")
            png_image.alpha_channel = "remove"
            png_image.save(file=png_stream)

    # Return PNG in base 64
    png_b64 = base64.b64encode(png_stream.getvalue()).decode("ascii")
    return render_template("divider.html", image_b64=png_b64)


@app.route("/submit_dividers", methods=["POST"])
def submit_dividers():
    global divider_ys
    divider_ys = request.json.get("dividerYs", [])
    print(divider_ys)
    return ""


if __name__ == "__main__":
    import sys
    app.run(host="localhost", port=int(sys.argv[1]) if len(sys.argv) > 1 else 8080, threaded=True)
