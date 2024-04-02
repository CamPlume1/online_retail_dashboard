from flask import Flask, Response
from flask_cors import CORS  # Import CORS from flask_cors module
from api_methods.component_calls import cam_test
from api_methods.test_graphic import gen_test_graphic
import matplotlib
from api_methods.mongo_api import visualize_spending

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


@app.route('/api/nick_graphic/')
def nick_graphic_endpoint() -> Response:
    return Response(visualize_spending(["Norway", "United Kingdom", "France", "Germany", "Australia"]), mimetype="image/png")


if __name__ == '__main__':
    app.run()
