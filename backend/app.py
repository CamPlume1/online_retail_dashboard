from flask import Flask, Response
from flask_cors import CORS  # Import CORS from flask_cors module
from api_methods.component_calls import cam_test
import matplotlib
from api_methods.mongo_api import visualize_spending
from api_methods.mongo_api import gen_country_graphic
from api_methods.mongo_api import best_selling_products

matplotlib.use('agg')

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes


@app.route('/')
def hello_world() -> str:
    return 'Hello World!'


@app.route('/cam/')
def cam_endpoint() -> str:
    return cam_test("cam")



@app.route('/api/nick_graphic/')
def nick_graphic_endpoint() -> Response:
    return Response(visualize_spending(["Norway", "United Kingdom", "France", "Germany", "Australia"]), mimetype="image/png")

@app.route('/tom_graphic/')
def test_tom_graphic() -> Response:

    figure = gen_country_graphic("Channel Islands")

    if figure == "Country Not Found":
        return "Country Not Found"
    else:

        return Response(figure, mimetype="image/png")

@app.route('/api/reece_graphic/')
def reece_graphic_endpoint() -> Response:
    figure = best_selling_products(2011)
    return Response(figure, mimetype="image/png")



if __name__ == '__main__':
    app.run()
