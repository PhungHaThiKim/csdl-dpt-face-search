from flask import Flask, render_template, send_from_directory

app = Flask(__name__, static_url_path='')

@app.route('/data/<path:path>')
def send_js(path):
    return send_from_directory('data', path)

@app.route("/")
def index():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(debug=True, port=5000)