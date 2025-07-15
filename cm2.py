def get_cm2_size(cm2_header) -> int:
    """
    Returns the size of the CM2 file based on the header.
    The header is expected to be a byte string.
    """

    if len(cm2_header) < 16:
        raise ValueError("Expected Cm2 header to be 16 bytes.")

    # Cm2 size appears in two places in the header:
    # - cm2_header[6:8] (big-endian)
    # - cm2_header[10:12] (big-endian)
    cm2_size_1 = int.from_bytes(cm2_header[6:8], byteorder='big')
    cm2_size_2 = int.from_bytes(cm2_header[10:12], byteorder='big')

    if cm2_size_1 != cm2_size_2:
        raise ValueError("Cm2 size mismatch in header.")
    
    return cm2_size_1

def sanatise_track_name(track_name: str) -> str:
    """
    Returns a sanatised version of the track name.
    Removes spaces, special characters (except underscore), and converts to uppercase.
    """

    # Remove spaces and special characters, keep only alphanumeric and underscores, convert to uppercase
    file_name = ''.join(c for c in track_name if c.isalnum() or c == '_').upper()
    return file_name

class CM2:
    def __init__(self, cm2_binary_data: bytes):
        self._track_name_bytes : bytes = self._get_track_name(cm2_binary_data)

        self.unique_id : str = self._get_unique_id(cm2_binary_data)
        self.track_name : str = self._track_name_bytes.decode('utf-8', errors='replace')
        self.description : str = self._get_description(self._track_name_bytes, cm2_binary_data)

    def _get_track_name(self, cm2_binary_data: bytes) -> str:
        """
        Returns the track name from the CM2 header.
        The track name is expected to be a byte string of length 36.
        """

        name_start_pos = 44
        name_bytes = bytearray()
        for b in cm2_binary_data[name_start_pos:]:
            if b == 0:
                break
            name_bytes.append(b)
        return name_bytes

    def _get_description(self, track_name_bytes: bytes, cm2_binary_data: bytes) -> str:
        """
        Returns the track description from the CM2 header.
        The description is expected to be a byte string of length 64.
        """

        # We use the track name as an anchor to find the second occurance.
        # Hacky solutions until the CM2 format is fully understood.
        first_pos = cm2_binary_data.find(track_name_bytes)
        if first_pos == -1:
            raise ValueError("Track name not found in CM2 data.")

        second_pos = cm2_binary_data.find(track_name_bytes, first_pos + 1)
        if second_pos == -1:
            raise ValueError("Second occurrence of track name not found in CM2 data.")

        description_pos = second_pos + len(track_name_bytes) + 1  # +1 to skip the null terminator

        # Like the track name we continue until we hit a null byte.
        description_bytes = bytearray()
        for b in cm2_binary_data[description_pos:]:
            if b == 0:
                break
            description_bytes.append(b)
        
        return description_bytes.decode('utf-8', errors='replace')
    
    def _get_unique_id(self, cm2_binary_data):
        """
        Returns the unique ID from the CM2 header.
        The unique ID is expected to be a byte string of length 8.
        The unique ID is located at bytes 112 to 116 in the CM2 header.
        """

        identifier = cm2_binary_data[112:116]
        return ''.join(f"{b:02X}" for b in identifier)