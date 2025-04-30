import mimetypes
import base64

def get_file_extension(base64_string: str) -> str:
    if base64_string.startswith("data:"):
        try:
            header = base64_string.split(";")[0]
            mime_type = header.split(":")[1]
            ext = mimetypes.guess_extension(mime_type)
            return ext if ext else ""
        except Exception:
            return ""
    return ""
