from flask import Blueprint, Response, request
import io
from .utils.ppm_converter import convert_ppm_to_png
from .utils.imgur import upload_to_imgur
from .utils.meta import publishToMeta

main = Blueprint("main", __name__)

@main.route("/hello")
def hello_world():
    return "<p>Hello, World!</p>"

@main.route("/convert", methods=["POST"])
def convert():
    ppm_file = request.files["file"]
    return convert_ppm_to_png(ppm_file)

@main.route("/upload-imgur", methods=["POST"])
def upload_imgur():
    png_data = request.files["file"]
    return upload_to_imgur(png_data)

@main.route('/convert-upload-imgur', methods=['POST'])
def convert_and_upload():
    data = request.data
    #Optionally write locally?
    # with open('received.ppm', 'wb') as f:
    #     f.write(data)

    png_data=convert_ppm_to_png(io.BytesIO(data)) 
    print("Successfully converted to png!")
    return upload_to_imgur(png_data) #return link
    
@main.route("/upload-meta", methods=["POST"])
def upload_meta():
    token=request.json['token']
    caption=request.json['caption']
    image_url=request.json['image_url']
    if (not token or not caption or not image_url):
        return Response(response="No token or caption or image url provided!",status=500)
    return publishToMeta('insta',token,caption,image_url)