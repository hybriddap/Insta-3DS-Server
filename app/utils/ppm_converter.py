from PIL import Image
import io
from flask import send_file

def convert_ppm_to_png(ppm_file):
    # If raw bytes provided, wrap in BytesIO
    if isinstance(ppm_file, (bytes, bytearray)):
        ppm_file2 = io.BytesIO(ppm_file)
    else:
        ppm_file2 = ppm_file

    # Ensure PIL reads from the start
    try:
        ppm_file2.seek(0)
    except Exception:
        pass

    image = Image.open(ppm_file2)
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output
    return send_file(output, mimetype="image/png")