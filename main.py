from app import app
import logging

# Setup logging for debugging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Log startup information
logger.info("Starting Term Sheet Validation application")

if __name__ == "__main__":
    # Run the Flask application with debug mode enabled
    # Binding to 0.0.0.0 makes the server accessible from other machines
    app.run(host="0.0.0.0", port=5000, debug=True)
