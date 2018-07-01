#!/usr/bin/env python3

import base64
from io import BytesIO
import os
import uuid
from flask import *
from wand.image import Image, Color

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.realpath(__file__)), "uploads/")
ALLOWED_EXTENSIONS = {"pdf"}

app = Flask(__name__, static_url_path="")
app.secret_key = b"\xd9h\xf8\xd2-\x8c\xe6\xdc;\r\xd9\x10'[\x03;"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# A fake 'database' that maps primary keys (array indices) to file names and divider Y coordinates
db = []


def is_allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def index():
    return render_template("submit_pdf.html")


def pdf_path_to_png_b64(pdf_path):
    # Convert to and save PNG to stream
    png_stream = BytesIO()
    with Image(filename=pdf_path, resolution=160) as pdf_image:
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
        return redirect(url_for("index"))
    pdf_file = request.files["file"]
    if not pdf_file or pdf_file.filename == "":
        flash("No file selected.")
        return redirect(url_for("index"))
    if not is_allowed_file(pdf_file.filename):
        flash("Invalid file. Must be a PDF.")
        return redirect(url_for("index"))
    pdf_filename = "{}.pdf".format(uuid.uuid4())
    session["pdf_filename"] = pdf_filename
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], pdf_filename)
    pdf_file.save(pdf_path)

    png_b64 = pdf_path_to_png_b64(pdf_path)
    return render_template("divider.html", image_b64=png_b64)


@app.route("/submit_dividers", methods=["POST"])
def submit_dividers():
    if "pdf_filename" not in session:
        flash("Need to create a submission.")
        return redirect(url_for("index"))
    db.append({"pdf_filename": session["pdf_filename"], "divider_ys": request.json.get("dividerYs", [])})
    print(db[-1])
    return jsonify({"submission_id": len(db) - 1})


@app.route("/divider_display/<int:submission_id>")
def divider_display(submission_id):
    if submission_id >= len(db):
        flash("Submission does not exist.")
        return redirect(url_for("index"))
    pdf_path = os.path.join(app.config["UPLOAD_FOLDER"], db[submission_id]["pdf_filename"])
    png_b64 = pdf_path_to_png_b64(pdf_path)
    return render_template("divider_display.html", image_b64=png_b64, divider_ys=db[submission_id]["divider_ys"])


if __name__ == "__main__":
    import sys
    app.run(host="localhost", port=int(sys.argv[1]) if len(sys.argv) > 1 else 8080, debug=True, threaded=True)
