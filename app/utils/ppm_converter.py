from PIL import Image
import io
from flask import send_file

def convert_ppm_to_png(ppm_file):
    image = Image.open(ppm_file.stream)
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return send_file(output, mimetype="image/png")