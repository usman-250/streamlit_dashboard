import os
from time import sleep
from flask import Flask, request, render_template, redirect,url_for,redirect

app = Flask(__name__)
app.config['UPLOAD_FOLDER']='/home/techverx/Desktop/web_app/uploads/'


@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if request.files['text']:
            txt=request.files['text']
            txt.save(os.path.join(app.config['UPLOAD_FOLDER']+'text/', txt.filename))
        
        if request.files.getlist('jd'):
            for jd in request.files.getlist('jd'):
                if jd.filename!='':
                    jd.save(os.path.join(app.config['UPLOAD_FOLDER']+'jd/', jd.filename))
        
        if request.files.getlist('resumes'):
            for f in request.files.getlist('resumes'):
                if f.filename!='':
                    f.save(os.path.join(app.config['UPLOAD_FOLDER']+'resumes/', f.filename))

        return 'Upload completed.'
    return render_template('h.html')

if __name__ == '__main__':
    app.run(debug = False)