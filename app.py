import os

import pandas as pd
import numpy as np
import SQLAlchemy

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

from flask import Flask, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

db = SQLAlchemy(app)

Base = automap_base()
Base.prepare(db.engine, reflect=True)

Samples = Base.classes.samples

@app.route("/")
def index():
    """Return to the homepage."""
    return render_template("index.html")


@app.route("/names")
def names():
    """Returns a list of names."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)
    return jsonify(list(df.columns)[2:])

@app.route("/samples/<sample>")
def samples(sample):
    """Return `otu_ids`, `otu_labels`, and `sample_values`."""
    stmt = db.session.query(Samples).statement
    df = pd.read_sql_query(stmt, db.session.bind)

    sample_data = df.loc[df[sample] > 1, ["otu_id", "otu_label", sample]]
    data = {
        "otu_ids": sample_data.otu_id.values.tolist(),
        "sample_values": sample_data[sample].values.tolist(),
        "otu_labels": sample_data.otu_label.tolist(),
    }
    return jsonify(data)



if __name__ == "__main__":
    app.run()