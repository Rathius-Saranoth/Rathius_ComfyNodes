# Import your custom node class(es) from their respective files
# This line imports your custom node class (e.g., LoadText) from another Python file within the same custom node directory (e.g., nodes.py).
from .nodes import *

# This tells ComfyUI to look for a 'js' folder in our directory
WEB_DIRECTORY = "js"

# (Optional) List the names that should be imported when using 'from package import *'
# This list defines the public interface of your module, specifying what names are imported when a user uses from your_module import *. While not strictly necessary for ComfyUI node registration, it's good practice for larger modules.
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']