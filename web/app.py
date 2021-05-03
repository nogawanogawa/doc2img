from flask import *
from werkzeug.utils import secure_filename
import os
from pathlib import Path
from pdf2image import convert_from_path
import datetime
import subprocess
import time
import requests

DEBUG = True

app = Flask(__name__)
app.config.from_object(__name__)

ALLOWED_EXTENSIONS = {'pdf', 'pptx'}

def dirCheck(new_path):
    if not os.path.exists(new_path):
        os.mkdir(new_path)

def isAllowedFile(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def isPDF(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pdf'}

def isPPTX(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'pptx'}

dirCheck("/tmp/pptx")
dirCheck("/tmp/pdf")
#dirCheck("/tmp/jpg")
dirCheck("/app/images/jpg")

@app.route('/', methods=['POST'])
def index():

    # atatched somthing?
    if 'file' not in request.files:
        return "no file\n"
    
    file = request.files['file']

    # atatched file?
    if file.filename == '':
        return 'No selected file\n'

    if not isAllowedFile(file.filename):
        return 'no allowed files\n'

    filename = secure_filename(file.filename)
    now = datetime.datetime.now()
    dtstr = now.strftime('%Y%m%d%H%M%S') # => '2019-08-02T02:20:43'
    dir_name = filename.split('.')[0] + "_" + dtstr
    

    if isPPTX(file.filename):
        output_path = os.path.join("/tmp/pptx", dir_name)
        dirCheck(output_path)
        file.save(os.path.join("/tmp/pptx", dir_name, filename))

        # pptx -> pdf
        output_path = os.path.join("/tmp/pdf", dir_name)
        dirCheck(output_path)

        res = subprocess.call(['libreoffice', '--headless', ' --nologo', '--nofirststartwizard', '--convert-to', 'pdf', '--outdir', output_path, os.path.join("/tmp/pptx", dir_name, filename)])
        
        # pdf -> jpg (recursive request)
        file = {'file': open(os.path.join("/tmp/pdf", dir_name, filename.split('.')[0] + '.pdf'), 'rb')}
        return requests.post('http://localhost:5000/', files=file).text

    elif isPDF(file.filename):
        output_path = os.path.join("/tmp/pdf", dir_name)
        dirCheck(output_path)
        file.save(os.path.join(output_path, filename))

        pdf_path = Path(os.path.join(output_path, filename))
        
        #output_path = os.path.join("/tmp/jpg", dir_name)
        output_path = os.path.join("/app/images/jpg", dir_name)
        
        dirCheck(output_path)

        convert_from_path(pdf_path, output_folder=output_path,fmt='jpeg',output_file=pdf_path.stem)
        return output_path

if __name__ == '__main__':
    app.run()