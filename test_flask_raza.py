"""Flask application."""

from os import sendfile
import os
from flask import Flask, jsonify, request, render_template, Response
from src.combine import get_lines, graph_lines
import googlemaps
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from dotenv import load_dotenv
import io

matplotlib.use("Agg")

load_dotenv()

app = Flask(__name__)


@app.route("/")
def hub():
    """Welcome page."""
    return render_template("hub.html")


@app.route("/NPRDirections")
def NPRDirections():
    """Input page for origin and destination."""
    return render_template("NPRDirections.html")


@app.route("/NPRDirections", methods=["POST"])
def NPRDirectionsResults():
    """Post image to user."""
    GMAPS_KEY = os.environ.get("GMAPS_KEY")
    NPR_KEY = os.environ.get("NPR_KEY")
    client = googlemaps.Client(key=GMAPS_KEY)
    origin = request.form["origin"]
    dest = request.form["dest"]
    gdf = get_lines(client, NPR_KEY, origin, dest)
    fig = graph_lines(gdf)
    fig = fig.figure
    output = io.BytesIO()
    FigureCanvasAgg(fig).print_png(output)
    return Response(output.getvalue(), mimetype="image/png")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
