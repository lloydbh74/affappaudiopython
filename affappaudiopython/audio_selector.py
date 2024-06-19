import os
import random
from pydub import AudioSegment
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Predefined directories
INTRO_DIR = "audio_files/intro"
OUTRO_DIR = "audio_files/outro"
MAIN_SECTION_DIR = "audio_files/main"
BACKGROUND_DIR = "audio_files/background"
OUTPUT_DIR = "output"  # Directory to save the final audio file - MAYBE ADD USER AND SESH ID SUB DIRECTORY

def select_audio_file(directory):
    """Select a random audio file from the specified directory."""
    try:
        abs_directory = os.path.abspath(directory)
        logging.info(f"Accessing directory: {abs_directory}")
        files = [f for f in os.listdir(directory) if f.endswith('.mp3')]
        logging.info(f"Files found in directory {directory}: {files}")  # Log the list of files
        if not files:
            raise FileNotFoundError(f"No audio files found in directory: {directory}")
        selected_file = os.path.join(directory, random.choice(files))
        logging.info(f"Selected file from {directory}: {selected_file}")
        return selected_file
    except Exception as e:
        logging.error(f"Error selecting audio file from {directory}: {str(e)}", exc_info=True)
        raise

def select_intro():
    """Select the intro audio file."""
    logging.info("Selecting intro audio file")
    return select_audio_file(INTRO_DIR)

def select_outro():
    """Select the outro audio file."""
    logging.info("Selecting outro audio file")
    return select_audio_file(OUTRO_DIR)


def select_main_sections(directory_path):
    """Select an even distribution of main section audio files."""
    logging.info("Selecting main section audio files")
    try:
        abs_directory = os.path.abspath(directory_path)
        logging.info(f"Accessing directory: {abs_directory}")
        files = [f for f in os.listdir(directory_path) if f.endswith('.mp3')]
        logging.info(f"Files found in directory {directory_path}: {files}")

        if not files:
            raise FileNotFoundError(f"No audio files found in directory: {directory_path}")

        # Calculate the number of files for even distribution
        num_files = len(files)
        if num_files == 0:
            raise FileNotFoundError(f"No audio files found in directory: {directory_path}")

        selected_files = [os.path.join(directory_path, file) for file in files]
        logging.info(f"Selected main section files: {selected_files}")
        return selected_files
    except Exception as e:
        logging.error(f"Error selecting main section audio files: {str(e)}", exc_info=True)
        raise



def select_background():
    """Select the background audio file."""
    logging.info("Selecting background audio file")
    return select_audio_file(BACKGROUND_DIR)

def overlay_audio(background_audio, main_sections):
    """Overlay main section audio files onto the background audio file at the correct timestamps."""
    try:
        logging.info(f"Background audio length: {len(background_audio)} ms")

        # Calculate the start times for the main sections to ensure even distribution
        main_section_count = len(main_sections)
        interval = (17 * 60 * 1000 - 3 * 60 * 1000) // main_section_count  # Total duration minus intro duration divided by number of sections

        for i, main_audio in enumerate(main_sections):
            logging.info(f"Main section {i+1} length: {len(main_audio)} ms")
            start_time = (4 * 60 * 1000) + (i * interval)  # Start at 4 minutes, then evenly distributed
            logging.info(f"Overlaying main section {i+1} at {start_time} ms")
            background_audio = background_audio.overlay(main_audio, position=start_time)
        return background_audio
    except Exception as e:
        logging.error(f"Error overlaying audio files: {str(e)}", exc_info=True)
        raise

def assemble_audio(intro, main_sections, outro, background):
    """Merge the intro, main section, outro, and background audio layers into a single continuous audio file."""
    try:
        logging.info("Loading intro audio file")
        intro_audio = AudioSegment.from_mp3(intro)
        logging.info(f"Intro audio length: {len(intro_audio)} ms")

        logging.info("Loading outro audio file")
        outro_audio = AudioSegment.from_mp3(outro)
        logging.info(f"Outro audio length: {len(outro_audio)} ms")

        logging.info("Loading background audio file")
        background_audio = AudioSegment.from_mp3(background)

        # Ensure the background audio is 20 minutes long
        if len(background_audio) < 20 * 60 * 1000:
            raise ValueError("Background audio is shorter than 20 minutes")

        # Overlay intro onto the background at the start
        final_audio = background_audio.overlay(intro_audio, position=0)

        # Load main sections as AudioSegment objects
        main_section_audios = [AudioSegment.from_mp3(section) for section in main_sections]

        # Overlay main sections onto the background
        final_audio = overlay_audio(final_audio, main_section_audios)
        logging.info(f"Final audio length before adding outro: {len(final_audio)} ms")

        # Add outro at the 17-minute mark
        outro_start_time = 17 * 60 * 1000  # 17 minutes in milliseconds
        logging.info(f"Overlaying outro at {outro_start_time} ms")
        final_audio = final_audio.overlay(outro_audio, position=outro_start_time)

        # Ensure the final audio is exactly 20 minutes long
        final_audio = final_audio[:20 * 60 * 1000]

        # Normalize audio levels
        final_audio = final_audio.normalize()

        return final_audio
    except Exception as e:
        logging.error(f"Error assembling audio files: {str(e)}", exc_info=True)
        raise

def export_audio(audio, output_path):
    """Export the merged audio file in MP3 format."""
    try:
        logging.info(f"Exporting audio to {output_path}")
        audio.export(output_path, format="mp3")
        logging.info(f"Audio exported successfully to {output_path}")
        return output_path
    except Exception as e:
        logging.error(f"Error exporting audio file: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    # Test the selection and assembly functions
    try:
        intro = select_intro()
        outro = select_outro()
        main_sections = select_main_sections()
        background = select_background()
        final_audio = assemble_audio(intro, main_sections, outro, background)
        export_path = os.path.join(OUTPUT_DIR, "final_audio.mp3")
        export_audio(final_audio, export_path)
        print("Audio assembly and export successful")
    except Exception as e:
        logging.error(f"Error during audio selection, assembly, and export test: {str(e)}", exc_info=True)