#!/usr/bin/env python3

import os
from flask import *
from werkzeug.utils import secure_filename
from wand.image import Image, Color

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uploads/")
print(UPLOAD_FOLDER)
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__, static_url_path="")
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def is_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
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

        # Convert to and save PNG
        png_filename = "{}.png".format(os.path.splitext(pdf_filename)[0])
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
                png_image.save(filename=os.path.join(app.config["UPLOAD_FOLDER"], png_filename))

        # TODO: redirect to divider page
    return render_template("submit_pdf.html")


if __name__ == "__main__":
    import sys
    app.run(host="localhost", port=int(sys.argv[1]) if len(sys.argv) > 1 else 8080, threaded=True)
