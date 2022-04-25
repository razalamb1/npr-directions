from flask import Flask, request, render_template, Response
from graphviz import render
from src.gmaps import get_directions
import googlemaps
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from dotenv import dotenv_values
import io


app = Flask(__name__)


@app.route("/")
def hub():
    return render_template("hub.html")


@app.route("/NPRDirections")
def NPRDirections():
    return render_template("NPRDirections.html")


@app.route("/NPRDirections", methods=["POST"])
def NPRDirectionsResults():
    config = dotenv_values(".env")
    GMAPS_KEY = config["GMAPS_KEY"]
    client = googlemaps.Client(key=GMAPS_KEY)
    input_dict = {
        "client": client,
        "origin": request.form["origin"],
        "dest": request.form["dest"],
    }
    fig = Figure()
    get_directions(input_dict).plot()
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")

    # return render_template("NPRDirectionsResults.html", final_output=map_output)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
