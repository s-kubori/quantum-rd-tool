"""Entry point that starts the metrics exporter before handing off to Streamlit.

Streamlit defers execution of app.py until a browser session connects, so an
import placed there does not bind the port at container startup. Importing
here, in the same process that Streamlit will run under, does.
"""

import sys

import utils.metrics  # noqa: F401  binds the metrics port
from streamlit.web import cli

if __name__ == "__main__":
    sys.argv = [
        "streamlit",
        "run",
        "app.py",
        "--server.address=0.0.0.0",
        "--server.port=8501"
    ]
    sys.exit(cli.main())
