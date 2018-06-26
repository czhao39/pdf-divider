#!/usr/bin/env python3

import base64
from io import BytesIO
import os
from flask import *
from werkzeug.utils import secure_filename
from wand.image import Image, Color

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uploads/")
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


def pdf_path_to_png_b64(pdf_path):
    # Convert to and save PNG to stream
    png_stream = BytesIO()
    with Image(filename=pdf_path) as pdf_image:
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
    return base64.b64encode(png_stream.getvalue()).decode("ascii")


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
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
    session["pdf_path"] = pdf_path
    pdf_file.save(pdf_path)

    png_b64 = pdf_path_to_png_b64(pdf_path)
    return render_template("divider.html", image_b64=png_b64)


@app.route("/submit_dividers", methods=["POST"])
def submit_dividers():
    global divider_ys
    divider_ys = request.json.get("dividerYs", [])
    print(divider_ys)
    return ""


@app.route("/divider_display")
def divider_display():
    # TODO: With actual DB, would use submission IDs instead of a temporary session.
    if "pdf_path" not in session:
        flash("Need to create a submission.")
        return redirect(request.url)

    png_b64 = pdf_path_to_png_b64(session["pdf_path"])
    return render_template("divider_display.html", image_b64=png_b64, divider_ys=divider_ys)


if __name__ == "__main__":
    import sys
    app.run(host="localhost", port=int(sys.argv[1]) if len(sys.argv) > 1 else 8080, threaded=True)
