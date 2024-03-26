from flask import Flask, Response
from api_methods.cam import cam_test
from api_methods.test_graphic import gen_test_graphic
import matplotlib.pyplot as plt

app = Flask(__name__)


@app.route('/')
def hello_world() -> str:  # put application's code here
    return 'Hello World!'


@app.route('/cam/')
def cam_endpoint() -> str:
    return cam_test("cam")


@app.route('/test_graphic/')
def test_graphic_enpoint() -> Response:
    return Response(gen_test_graphic(), mimetype="image/png")




if __name__ == '__main__':
    app.run()
