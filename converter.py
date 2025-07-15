import os
import shutil
import logging
import sys
from cm2 import CM2, get_cm2_size, sanatise_track_name
from utils import byte_to_int, get_folder_names, grab_specific_data, load_file

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def write_extracted_files(track_id: int, trk_data: bytes, cm2_data: bytes, nav_data: bytes, hud_data: bytes, console_output: callable, output_dir="output_test"):
    """
    Writes the extracted files to the output directory.
    The output directory will be created if it does not exist.
    """

    print("======================")

    logger.debug(f"Writing files for track ID: {track_id}")
    logger.debug(f"Length of server_trk_full: {len(trk_data)}")
    logger.debug(f"Length of server_cm2_full: {len(cm2_data)}")
    logger.debug(f"Length of server_nav_full: {len(nav_data)}")
    logger.debug(f"Length of server_hud_header: {len(hud_data)}")

    os.makedirs(output_dir, exist_ok=True)

    output_path = os.path.join(output_dir, track_id)
    os.makedirs(output_path, exist_ok=True)

    cm2_data_obj = CM2(cm2_data)
    track_unique_id = cm2_data_obj.unique_id
    track_name = cm2_data_obj.track_name
    track_description = cm2_data_obj.description

    print(f"Unique ID: {track_unique_id}")
    print(f"File Name: {track_name}")
    print(f"Track Description: {track_description}")

    console_output("======================")
    console_output(f"Unique ID: {track_unique_id}")
    console_output(f"File Name: {track_name}")
    console_output(f"Track Description: {track_description}")

    # File name must be exactly TRACKNAME_UNIQUEID or the game will remove the files
    base_filename = f"{sanatise_track_name(track_name)}_{track_unique_id}"
    with open(os.path.join(output_dir, track_id, f"{base_filename}.TRK"), "wb") as f:
        f.write(trk_data)
    with open(os.path.join(output_dir, track_id, f"{base_filename}.CM2"), "wb") as f:
        f.write(cm2_data)
    with open(os.path.join(output_dir, track_id, f"{base_filename}.NAV"), "wb") as f:
        f.write(nav_data)
    with open(os.path.join(output_dir, track_id, f"{base_filename}.HUD"), "wb") as f:
        f.write(hud_data)

    # Copy placeholder files for PNGs
    # Unfourtunately, we don't have the actual PNG files, so we use placeholders :(
    dst_small_png = os.path.join(output_path, f"{base_filename}_SMALL.PNG")
    dst_png = os.path.join(output_path, f"{base_filename}.PNG")

    # Determine resource path depending on execution context (PyInstaller or normal Python)
    if getattr(sys, 'frozen', False):
        # Running in a PyInstaller bundle
        resource_dir = os.path.join(sys._MEIPASS, "resources")
    else:
        # Running in normal Python
        resource_dir = "resources"

    shutil.copy(os.path.join(resource_dir, "PLACEHOLDER_XXXXXXX_SMALL.PNG"), dst_small_png)
    shutil.copy(os.path.join(resource_dir, "PLACEHOLDER_XXXXXXX.PNG"), dst_png)

    print("Successfully written files to output directory.")

def convert_files(archive_path: str, output_path: str, console_output: callable):
    """
    Converts the files from the archive path to the output path.
    This function is a placeholder for the actual conversion logic.
    """

    print("Starting conversion...")
    print(f"Archive path: {archive_path}"
          f"\nOutput path: {output_path}")

    # Directory where server files are located
    server_folders = get_folder_names(archive_path)

    if not server_folders:
        logger.debug("No server folders found. Please check the server_files directory.")
        console_output("No server folders found. Please check the server_files directory.")
    else:
        logger.debug(f"Server folders found: {server_folders}")
        console_output(f"Server folders found: {server_folders}")

    cm2s_ = []
    for server_folder in server_folders:
        binary_path = os.path.join(archive_path, server_folder, "data.bin")
        if not os.path.isfile(binary_path):
            logger.warning(f"data.bin not found in {os.path.join(archive_path, server_folder)}. Skipping.")
            console_output(f"data.bin not found in {os.path.join(archive_path, server_folder)}. Skipping.")
            continue
        
        server_binary_file = load_file(binary_path)

        # Full CTH extraction
        logger.debug("CTH EXTRACTION ====")
        # First 4 bytes are the same
        server_cth_start_pos = 0 # Assuming CTH starts at the beginning of the file
        server_cth_end_pos = 20  # Assuming a fixed size for CTH header
        server_cth_header = grab_specific_data(server_binary_file, start_pos=server_cth_start_pos, end_pos=server_cth_end_pos) # CTH header is at the start of the file
        nav_file_size = byte_to_int(grab_specific_data(server_binary_file, start_pos=12, end_pos=16,)) # NAV file size is at offset 12-16 in CTH header
        logger.debug(f"Server NAV file size: {nav_file_size}")

        # Full trk extraction
        logger.debug("TRK EXTRACTION ====")
        server_trk_start_pos = server_cth_end_pos # TRK starts right after CTH
        server_trk_size = byte_to_int(grab_specific_data(server_binary_file, start_pos=server_trk_start_pos + 20, end_pos=server_trk_start_pos + 24)) # TRK size is at offset 20-24 in TRK header
        server_trk_end_pos = server_trk_start_pos + server_trk_size
        server_trk_full = grab_specific_data(server_binary_file, start_pos=server_trk_start_pos, end_pos=server_trk_end_pos)

        # Full end to end server cm2 extraction
        logger.debug("CM2 EXTRACTION ====")
        server_cm2_start_pos = server_trk_start_pos + server_trk_size # CM2 starts right after TRK
        server_cm2_header = grab_specific_data(server_binary_file, start_pos=server_cm2_start_pos, end_pos=server_cm2_start_pos + 16)
        server_cm2_size = get_cm2_size(server_cm2_header[:16]) + 16  # Adding 16 for the header size
        logger.debug(f"Server CM2 size: {server_cm2_size}")
        server_cm2_end_pos = server_cm2_start_pos + server_cm2_size
        server_cm2_full = grab_specific_data(server_binary_file, start_pos=server_cm2_start_pos, end_pos=server_cm2_end_pos)

        # Full end to end server nav extraction
        logger.debug("NAV EXTRACTION ====")
        server_nav_start_pos = server_cm2_end_pos
        server_nav_end_pos = nav_file_size + server_nav_start_pos # NAV starts right after CM2 and goes to the size specified in CTH
        logger.debug(f"Server start position: {server_nav_start_pos}")
        logger.debug(f"Server NAV end position: {server_nav_end_pos}")
        server_nav_full = grab_specific_data(server_binary_file, start_pos=server_nav_start_pos, end_pos=server_nav_end_pos)

        # Full end to end extract hud file
        logger.debug("HUD EXTRACTION ====")
        server_hud_start_pos = server_nav_end_pos
        server_hud_end_pos = len(server_binary_file)  # Assuming hud file goes to the end of the binary data
        server_hud_full = grab_specific_data(server_binary_file, start_pos=server_hud_start_pos, end_pos=server_hud_end_pos)

        # Write the extracted files to the output directory
        write_extracted_files(
            track_id=server_folder,
            trk_data=server_trk_full,
            cm2_data=server_cm2_full,
            nav_data=server_nav_full,
            hud_data=server_hud_full,
            output_dir=output_path,
            console_output=console_output
        )

        cm2s_.append(server_cm2_full)