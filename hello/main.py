from flask import render_template
from flask import Flask
from waitress import serve



app = Flask(__name__)
@app.route('/')
def index():
    return render_template('testapp/index.html')

if __name__ == '__main__':
    serve(app, host='0.0.0.0', port=5000)

#更新test