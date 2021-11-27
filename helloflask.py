from flask import Flask, flash, render_template, request, send_file, abort
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)

if not os.path.exists('/root/new_uploads'):
	os.mkdir('/root/new_uploads')

uploader = '/root/new_uploads/'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
def authorized(f):
    return '.' in f and \
           f.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

app.config['UPLOAD_FOLDER'] = uploader

@app.route('/')
def upload_file():
	return render_template('index.html')

@app.route('/upload', methods=['GET', 'POST'])
def uploadfile():
	if request.method == 'POST':
        	f = request.files['file']
	if f and authorized(f.filename):
		f.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(f.filename)))
		return 'File Uploaded!'
	else:
		abort(400)

@app.route("/downloadfile/<filename>", methods=['GET'])
def download_file(filename):
	return render_template('download.html', value=filename)

@app.route('/api/<filename>', methods=['GET'])
def download(filename):
	file_path = uploader + filename
	return send_file(file_path, as_attachment=True, attachment_filename='')

if __name__=='__main__':
	app.run(host='0.0.0.0', debug=True)
