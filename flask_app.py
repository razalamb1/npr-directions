"""Flask application."""

import os
from flask import Flask, request, render_template
from src.npr import StationError
from src.gmaps import OutsideUSA
from src.combine import get_lines, graph_lines
import googlemaps
import matplotlib
from matplotlib.figure import Figure
from dotenv import load_dotenv
import io
import base64

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
    try:
        try:
            gdf = get_lines(client, NPR_KEY, origin, dest)
        except OutsideUSA:
            outsideUSA_error = "Address must be within the US!"
            return render_template(
                "OutsideUSA_ErrorMessage.html", outsideUSA_error=outsideUSA_error
            )
    except StationError:
        station_error = "There is no NPR station found near your starting location, or the NPR API has reached its daily maximum. Please try a different starting location or try again tomorrow. "
        return render_template(
            "NPRStation_ErrorMessage.html", station_error=station_error
        )
    fig = Figure()
    fig = graph_lines(gdf)
    output = io.BytesIO()
    fig.savefig(output, format="png", dpi=300, bbox_inches="tight", pad_inches=1)
    final_plot = base64.b64encode(output.getbuffer()).decode("utf-8")
    return render_template("NPRDirectionsResults.html", img_data=final_plot)


@app.route("/OutsideUSAErrorMessage")
def OutsideUSA_ErrorMessage():
    """Error message if user entered wrong information."""
    return render_template("OutsideUSA_ErrorMessage.html")


@app.route("/NPRStationErrorMessage")
def NPRStation_ErrorMessage():
    """Error message if station is not found or API reached daily limit."""
    return render_template("NPRStation_ErrorMessage.html")


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8080, debug=False)
