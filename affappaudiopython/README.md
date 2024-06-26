# AffAppAudioPython

AffAppAudioPython is a Python-based application designed to create unique 20-minute meditation/hypnotherapy audio files by combining various audio elements. The application uses a webhook to trigger the process, selects and combines audio files, and exports the final product in MP3 format. The originator application generates the affirmation audio and deposits it on the server in sub directories based on `user_id_sesh_id` structure. This creates uniques audio files based on the originator app users preferences.

## Overview

The AffAppAudioPython application architecture is built around a Flask-based web server that handles webhook requests. The application performs the following tasks:

1. **Webhook Integration**: A Flask web server receives and validates incoming webhook requests.
2. **Audio Selection**: The application selects intro, outro, main section, and background audio files from predefined directories.
3. **Layer Integration**: The selected audio files are combined using the `pydub` library.
4. **Audio Assembly**: The combined audio layers are merged into a single continuous audio file.
5. **Export**: The final audio file is exported in MP3 format.
6. **Response Handling**: The application sends a response back to the webhook with the status and a link to the generated audio file.

### Technologies Used

- **Python**: The core programming language used for the application.
- **FFmpeg**: Required by `pydub` to handle audio file manipulations.
- **Flask**: Web framework for handling web requests.
- **pydub**: Library for manipulating audio files.
- **requests**: Library for handling HTTP requests.
- **gunicorn**: WSGI HTTP server for deploying the Flask application.

### Project Structure

- `app.py`: Defines the Flask application and implements webhook handling.
- `audio_selector.py`: Contains functions to select and overlay audio files.
- `audio files`: Is the Main file directory where the audio files are stored
- `audio files>background`: Is the file sub directory where the background audio files are stored
- `audio files>intro`: Is the file sub directory where the intro audio files are stored
- `audio files>main`: Is the file sub directory where the affirmation audio files are stored
- `audio files>main>user_id_sesh_id`: Is the dynamic file sub directory where the affirmation audio files are stored for each generated session.
- `audio files>outro`: Is the file sub directory where the outro audio files are stored


## Features

- **Webhook Integration**: Receives and validates incoming requests to trigger the audio creation process.
- **Audio Selection**: Randomly selects intro, outro, main section, and background audio files from predefined directories.
- **Layer Integration**: Combines selected audio files seamlessly.
- **Audio Assembly**: Merges the combined layers into a single continuous audio file of exactly 20 minutes.
- **Export**: Exports the final audio file in MP3 format.
- **Response Handling**: Sends a response back to the webhook with the status and a link to the generated audio file.

## Getting Started

### Requirements

- Python 3.x
- FFmpeg
- Required Python libraries: Flask, pydub, requests, gunicorn

### Quickstart

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd AffAppAudioPython
    ```

2. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

3. **Ensure FFmpeg is installed**:
    - On macOS: `brew install ffmpeg`
    - On Ubuntu: `sudo apt-get install ffmpeg`
    - On Windows: Download from [FFmpeg official website](https://ffmpeg.org/download.html) and follow the installation instructions.

4. **Run the Flask application**:
    ```sh
    python app.py
    ```

5. **Test the webhook endpoint**:
    - Send a POST request to `http://localhost:8000/webhook` with the required JSON payload, including fields such as `request_id`, `user_id`, `sesh_id`, `timestamp`, and `callback_url`.
#### Example Request
```
{
  "request_id": "4321",
  "user_id": "user456",
  "sesh_id": "sesh9",
  "timestamp": "2024-06-18T10:00:00Z",
  "callback_url": "http://example.com/callback"
}
```

### Notes

- Ensure that the directories for intro, outro, main sections, and background audio files (`audio_files/intro`, `audio_files/outro`, `audio_files/main`, `audio_files/background`) exist and contain `.mp3` files.
- The application logs information to both the console and a log file for easier debugging and monitoring.

#### Error logs

| Error Message                                            | Function Name                | Meaning                                                                 |
|----------------------------------------------------------|------------------------------|-------------------------------------------------------------------------|
| Invalid JSON received                                    | webhook                      | The incoming webhook request does not contain valid JSON.               |
| Missing field: {field}                                   | webhook                      | The incoming webhook request is missing a required field.               |
| File not found error: {str(fnf_error)}                   | webhook                      | A required audio file could not be found during processing.             |
| Error processing webhook: {str(e)}                       | webhook                      | An unspecified error occurred during the processing of the webhook request. |
| No audio files found in directory: {directory}           | select_audio_file            | The specified directory does not contain any audio files.               |
| Error selecting audio file from {directory}: {str(e)}    | select_audio_file            | An error occurred while selecting an audio file from the specified directory. |
| Error selecting main section audio files: {str(e)}       | select_main_sections         | An error occurred while selecting main section audio files.             |
| Error selecting background audio file: {str(e)}          | select_background            | An error occurred while selecting a background audio file.              |
| Error assembling audio files: {str(e)}                   | assemble_audio               | An error occurred while assembling the audio files into a final audio track. |
| Error exporting audio file: {str(e)}                     | export_audio                 | An error occurred while exporting the final audio file to the specified path. |
| Error during audio selection, assembly, and export test: {str(e)} | __main__ (in audio_selector.py) | An error occurred during the test of audio selection, assembly, and export functions. |

This table should help in understanding where and what kind of errors might occur in the application, allowing for easier debugging and maintenance.


### License

```
Copyright (c) 2024.
```