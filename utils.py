import os

def byte_to_int(byte_data: bytes, byteorder: str = 'big', signed: bool = False) -> int:
    """
    Converts a bytes object (of length 1 or more) into an integer.
    """

    return int.from_bytes(byte_data, byteorder=byteorder, signed=signed)

def compare_binary_files(file1: bytes, file2: bytes) -> tuple:
    """
    Compares two binary files (bytes objects).
    Returns two lists:
      - matching_indices: positions where bytes are the same
      - differing_indices: positions where bytes differ
    Stops at the end of the shorter file.
    """

    matching_indices = []
    differing_indices = []
    min_len = min(len(file1), len(file2))
    for i in range(min_len):
        if file1[i] == file2[i]:
            matching_indices.append(i + 1)
        else:
            differing_indices.append(i + 1)
    return matching_indices, differing_indices

def convert_hex_to_string(binary_data: bytes) -> str:
    """
    Converts binary data to a string representation.
    """

    return ''.join(chr(byte) if 32 <= byte <= 126 else '.' for byte in binary_data)

def binary_to_hex_string(binary_data: bytes) -> list[str]:
    """
    Converts binary data to a list of hex strings.
    Each byte is represented as a two-character hex string.
    """

    header = [f"{byte:02x}" for byte in binary_data]
    return header

def load_file(file_path: str) -> bytes:
    """
    Loads a binary file and returns its content as bytes.
    """

    with open(file_path, 'rb') as file:
        return file.read()

def get_folder_names(directory: str) -> list[str]:
    """
    Returns a list of folder names in the specified directory.
    Parameters:
        - directory: The path to the directory to search for folders.
    Returns:
        - A list of folder names (not full paths).
    """

    return [name for name in os.listdir(directory)
            if os.path.isdir(os.path.join(directory, name))]
    
def grab_specific_data(binary_file: bytes, start_pos: int = 0, end_pos: int = 0, print_: bool = False) -> bytes:
    """
    Grabs specific data from a binary file.
    Parameters:
        - binary_file: The binary file as a bytes object.
        - start_pos: The starting position (byte offset) to grab data from.
        - end_pos: The ending position (byte offset) to grab data to. If 0, grabs to the end of the file.
        - print_: If True, prints the hex and string representation of the grabbed data.

    Returns:
        - The grabbed data as a bytes object.
    """

    if end_pos == 0:
        end_pos = len(binary_file)
        
    if end_pos > len(binary_file):
        raise ValueError("end_pos exceeds the length of the binary file.")
    
    if print_:
        header = binary_to_hex_string(binary_file[start_pos:end_pos])
        header_string = convert_hex_to_string(binary_file[start_pos:end_pos])
        print(f"Hex: {header}")
        print(f"String: {header_string}")
        
    return binary_file[start_pos:end_pos]

def find_occurrences_in_hex_target(target_hex: list[str], search_hex: list[str]) -> list[int]:
    """
    Returns a list of byte positions where search_hex occurs in target_hex.
    Both arguments should be hex strings (e.g., '4d5a').
    """
    
    occurrences = []
    search_len = len(search_hex)
    for i in range(len(target_hex) - search_len + 1):
        if target_hex[i:i + search_len] == search_hex:
            occurrences.append(i)  # Each byte is two hex chars
    return occurrences