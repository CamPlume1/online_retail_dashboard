from flask import Flask, Response, request
from flask_cors import CORS
from api_methods.component_calls import cam_test, total_transactions, total_sales, total_units, top_unit, top_unit_rev, \
    cam_viz, unique_descriptions
import matplotlib
from api_methods.mongo_api import plot_country_spending, gen_time_series_graphic, get_unique_countries
from api_methods.mongo_api import gen_time_series_graphic, plot_country_spending
from api_methods.mongo_api import gen_country_graphic
from api_methods.mongo_api import best_selling_products
from api_methods.component_calls import countries, years

# Created by Cam Plume

# Global Environment Specs
matplotlib.use('agg')

app = Flask(__name__)
CORS(app)


# Cam's graphic replacing Andrews
@app.route('/api/cam_graphic/', methods=['GET'])
def cam_graphic_endpoint():
    exclusion = request.args.get('descriptions').split(',')
    exclusion_upper = [x.upper() for x in exclusion]
    if '' in exclusion_upper:
        exclusion_upper.remove('')
    return Response(cam_viz(exclusion_upper), mimetype="image/png")


# API Root function for testing
@app.route('/')
def hello_world() -> str:
    return 'Hello World!'


# Early function for testing string return format
@app.route('/cam/')
def cam_endpoint() -> str:
    return cam_test("cam")


# Gets all the years in the dataset
@app.route('/years/')
def year_endpoint() -> list[str]:
    return years()


# Gets Nick's graphic
@app.route('/api/nick_graphic/', methods=['GET'])
def nick_graphic_endpoint() -> Response:
    country_list = request.args.get('countries').split(',')
    return Response(plot_country_spending(country_list), mimetype="image/png")


# Gets Tom's Graphic
@app.route('/tom_graphic/', methods=['GET'])
def test_tom_graphic() -> Response:
    country = request.args.get('country')

    figure = gen_country_graphic(country)

    if figure == "Country Not Found":
        return "Country Not Found"
    else:

        return Response(figure, mimetype="image/png")


# Gets Tom's Graphic
@app.route('/test_get/', methods=['GET'])
def test_get() -> Response:
    country = request.args.get('country')

    figure = gen_country_graphic(country)
    return country


# Gets Reece's graphic
@app.route('/api/reece_graphic/', methods=['GET'])
def reece_graphic_endpoint() -> Response:
    year = request.args.get('year')
    figure = best_selling_products(int(year))
    return Response(figure, mimetype="image/png")


# Gets all the countries in the dataset
@app.route('/api/countries')
def countries_endpoint():
    return countries()


# Gets the number of unique countries in the dataset
@app.route('/api/countries_count')
def countries_count_endpoint():
    return str(len(countries()))


# Gets the total number of transactions in the database
@app.route('/api/total_transactions')
def transactions_endpoint():
    return str(total_transactions())


# gets the total sales in dollars from the database
@app.route('/api/total_sales')
def sales_endpoint():
    return str(total_sales())

@app.route('/api/unique_descriptions')
def unique_descriptions_endpoint():
    return unique_descriptions()


# gets the total number of units sold
@app.route('/api/total_units')
def units_endpoint():
    return str(total_units())


# Gets the unit purchased most (by quantity)
@app.route('/api/top_unit')
def top_unit_endpoint():
    return str(top_unit()).replace(' ', '')


# Gets the unit that generates the most revenue
@app.route('/api/top_unit_rev')
def top_by_rev_endpoint():
    return top_unit_rev()


# Stub- Not complete yet
@app.route('/api/top_country')
def top_country_endpoint():
    return top_unit()


# Gets andrews graphic
@app.route('/api/andrew_graphic/')
def andrew_graphic_endpoint() -> Response:
    figure = gen_time_series_graphic()
    return Response(figure, mimetype="image/png")




if __name__ == '__main__':
    app.run()
