import mimetypes
from os import sendfile
from flask import Flask, jsonify, request, render_template, Response
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
    #     config = dotenv_values(".env")
    #     GMAPS_KEY = config["GMAPS_KEY"]
    #     client = googlemaps.Client(key=GMAPS_KEY)
    origin = request.form["origin"]
    dest = request.form["dest"]
    # fig = get_directions(client, origin, dest).plot(figsize=(20, 20))
    # fig = fig.figure()
    # output = io.BytesIO()
    # FigureCanvasAgg(fig).print_png(output)
    # direction_plot = Response(output.getvalue(), mimetype="image/png")
    final_output = f"Origin: {origin}, Destination: {dest}"
    return render_template("NPRDirectionsResults.html", final_output=final_output)
    # canvas = FigureCanvasAgg(fig)
    # img = io.BytesIO()
    # fig.(img)
    # img.seek(0)
    # return render_template("NPRDirectionsResults.html", direction_plot=direction_plot)
    # return render_template("NPRDirectionsResults.html", final_output=map_output)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
