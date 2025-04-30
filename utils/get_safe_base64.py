import base64

def get_safe_base64(data: str) -> bytes:
    if "," in data:
        data = data.split(",", 1)[1]
    # Add padding if needed
    padding_needed = 4 - (len(data) % 4)
    if padding_needed and padding_needed != 4:
        data += "=" * padding_needed
    return base64.b64decode(data)
