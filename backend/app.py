from flask import Flask, Response
from flask_cors import CORS  # Import CORS from flask_cors module
from api_methods.cam import cam_test
from api_methods.test_graphic import gen_test_graphic
import matplotlib

matplotlib.use('agg')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/')
def hello_world() -> str:
    return 'Hello World!'


@app.route('/cam/')
def cam_endpoint() -> str:
    return cam_test("cam")


@app.route('/api/test_graphic/')
def test_graphic_enpoint() -> Response:
    return Response(gen_test_graphic(), mimetype="image/png")


if __name__ == '__main__':
    app.run()
