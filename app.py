from flask import Flask, render_template, request, redirect, url_for
import os

from converter.converter import Converter

app = Flask(__name__)

app.config['FILE_UPLOADS'] = "C:\\Users\\USER\\Downloads\\proggraming stuff\\umltocode\\uploads"

code = ""

@app.route('/', methods=['GET', 'POST'])
def index():
    global code
    if request.method == 'POST':
        uploaded_file = request.files['file']
        filepath = os.path.join(app.config['FILE_UPLOADS'], uploaded_file.filename)
        uploaded_file.save(filepath)
        pr =  request.form.get('pl')
        print(pr)
        converter = Converter(pr)
        code = converter.getCode(filepath)
        return redirect(url_for('result'))
    return render_template('index.html', code=code)

@app.route('/result')
def result():
    print(code)
    return render_template('result.html', code=code)

@app.route('/more')
def more():
    print(code)
    return render_template('more.html', code=code)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
