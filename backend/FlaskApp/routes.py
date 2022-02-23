from flask import request, render_template, make_response, jsonify, redirect, url_for
from flask import current_app as app
from werkzeug.utils import secure_filename
import os
import base64 
import cv2


from .inference import inference

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = 'static/temp'
INFERENCE_OUTPUT_FOLDER = os.path.join(ROOT_DIR, 'static/output')
ALLOWED_EXTENSIONS = {'jpg', 'jpeg'}


@app.route('/', methods=['GET'])
def load_home_page():

    # Return home page
    return render_template('index.html')


@app.route('/', methods=['POST'])
def run_prediction():

    print(request.files)
    if 'file' not in request.files:
        print('File Not Uploaded')
        return

    # Get category of prediction
    file = request.files['file']
    category, input_img, overlay = inference(file)

    # # Get category of prediction
    # imgFullPath = os.path.join(ROOT_DIR, 'static/test_images/DME-1081406-1.jpeg')
    # category, input_img, overlay = inference(imgFullPath)

    cv2.imwrite(os.path.join(ROOT_DIR, 'static/output/overlay.jpeg'), overlay)

    # Render the result template
    return render_template('result.html', category=category)

@app.route("/sample/images", methods=["GET"])
def get_sample_images():

    # dev-anil/ML-Samsung-OCT/backend/FlaskApp/static/test_images/
    data = {
        "images": [{
            "img_name": "CNV-1016042-1.jpeg",
            "class": "CNV",
            "img_path": "/assets/test_images/CNV-1016042-1.jpeg",
            "prediction_img_path": "/assets/test_images/CNV-1016042-1-overlay.jpeg"
        }, {
            "img_name": "DME-1081406-1.jpeg",
            "class": "DME",
            "img_path": "/assets/test_images/DME-1081406-1.jpeg",
            "prediction_img_path": "/assets/test_images/DME-1081406-1-overlay.jpeg"
        }, {
            "img_name": "DRUSEN-1083159-1.jpeg",
            "class": "DRUSEN",
            "img_path": "/assets/test_images/DRUSEN-1083159-1.jpeg",
            "prediction_img_path": "/assets/test_images/DRUSEN-1083159-1-overlay.jpeg"
        }, {
            "img_name": "NORMAL-1017237-1.jpeg",
            "class": "NORMAL",
            "img_path": "/assets/test_images/NORMAL-1017237-1.jpeg",
            "prediction_img_path": "/assets/test_images/NORMAL-1017237-1-overlay.jpeg"
        }]
    }

    res = make_response(jsonify(data), 200)

    return res


@app.route("/upload/image", methods=["POST"])
def upload_file():
    if request.method == 'POST':

        # check if the post request has the file part
        if 'file' not in request.files:
            return make_response(jsonify({
                "error": "No files uploaded",
                "success": False
            }), 400)

        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            return make_response(jsonify({
                "error": "Empty file selected",
                "success": False
            }), 400)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
            tmp_file_path = os.path.join(ROOT_DIR, UPLOAD_FOLDER, filename)
            print("ROOT_DIR:" + ROOT_DIR)
            print("tmp_file_path:" + tmp_file_path)
            file.save(tmp_file_path)
            # return redirect(url_for('download_file', name=filename))

            category, input_img, overlay = inference(tmp_file_path)

            overlay_file_name = "overlay_" + filename
            overlay_full_path = os.path.join(INFERENCE_OUTPUT_FOLDER, overlay_file_name)
            cv2.imwrite(overlay_full_path, overlay)

            # img = cv2.imread(overlay_full_path)
            # _, im_arr = cv2.imencode('.jpg', img)  # im_arr: image in Numpy one-dim array format.
            # im_bytes = im_arr.tobytes()
            # im_b64 = base64.b64encode(im_bytes)
            #print(im_b64)

            return make_response(jsonify({
                "error": "",
                "success": True,
                "data": {
                    "category": category,
                    "input": "",
                    "predicted_output": overlay_full_path
                }
            }), 200)
        
        return make_response(jsonify({
            "error": "Unknown error",
            "success": False
        }), 500)


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
