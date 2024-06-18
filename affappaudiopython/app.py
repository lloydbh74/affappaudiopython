from flask import Flask, request, jsonify
import logging
import os
from audio_selector import select_intro, select_outro, select_main_sections, select_background, assemble_audio, export_audio

app = Flask(__name__)

# Set up logging to a file and console
logging.basicConfig(
    level=logging.INFO,  # Log level
    format='%(asctime)s %(levelname)s: %(message)s',  # Log format
    datefmt='%Y-%m-%d %H:%M:%S'  # Date format
)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s'))
logging.getLogger().addHandler(console_handler)

@app.route("/ping")
def ping():
    return {"message": "pong"}, 200

@app.route("/webhook", methods=["POST"])
def webhook():
    try:
        logging.info("Received webhook request")
        data = request.get_json()
        logging.info(f"Request data: {data}")
        if not data:
            logging.error("Invalid JSON received")
            return jsonify({"error": "Invalid JSON"}), 400

        # Validate necessary fields
        required_fields = ["request_id", "user_id", "sesh_id", "timestamp", "callback_url"] # Replace with actual field names
        for field in required_fields:
            if field not in data:
                logging.error(f"Missing field: {field}")
                return jsonify({"error": f"Missing field: {field}"}), 400

        # Audio processing
        logging.info("Starting audio processing")
        intro = select_intro()
        logging.info(f"Selected intro: {intro}")
        outro = select_outro()
        logging.info(f"Selected outro: {outro}")
        main_sections = select_main_sections()
        logging.info(f"Selected main sections: {main_sections}")
        background = select_background()
        logging.info(f"Selected background: {background}")
        final_audio = assemble_audio(intro, main_sections, outro, background)
        
        # ADD THE WEBHOOK FIELDS TO THE NAME
        output_filename = f"affirmation_{data['request_id']}_{data['user_id']}_{data['sesh_id']}.mp3"
        output_path = os.path.join("output", output_filename)
        export_audio(final_audio, output_path)

        # If processing is successful
        logging.info("Audio processing completed successfully")
        return jsonify({"message": "Audio processing completed successfully", "file_link": output_path}), 200
    except FileNotFoundError as fnf_error:
        logging.error(f"File not found error: {str(fnf_error)}", exc_info=True)
        return jsonify({"error": str(fnf_error)}), 404
    except Exception as e:
        logging.error(f"Error processing webhook: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=8000)  # Enable debug mode and ensure not to use port 5000