from flask import Flask, render_template, make_response

app = Flask(__name__, static_url_path='/static')
app.url_map.strict_slashes = False

@app.route('/')
def index():
    return render_template("index.html")

def static_file(path):
    return app.send_static_file(path)

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0', port=80)
