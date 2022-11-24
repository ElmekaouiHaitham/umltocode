from flask import Flask, render_template, request, redirect, url_for
import os

from converter.converter import Converter

app = Flask(__name__)

app.config['FILE_UPLOADS'] = "uploads"

code = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    global code
    if request.method == 'POST':
        try:
            uploaded_file = request.files['file']
            filepath = os.path.join(app.root_path, app.config['FILE_UPLOADS'], uploaded_file.filename)
            uploaded_file.save(filepath)
            pr =  request.form.get('pl')
            converter = Converter(pr)
            code = converter.getCode(filepath)
        except Exception as e:
            code = ["error: \n"+str(e)]
        return redirect(url_for('result'))
    return render_template('index.html')

@app.route('/result')
def result():
    if code == "":
        return render_template('index.html')
    return render_template('result.html', code=code)

@app.route('/coming')
def coming():
    return render_template('comingsoon.html')

@app.route('/features')
def features():
    return render_template('features.html')

@app.route('/more')
def more():
    return render_template('more.html')

@app.route('/examples')
def examples():
    return render_template('examples.html')

@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
