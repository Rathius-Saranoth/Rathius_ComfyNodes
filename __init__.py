# Import our node classes
from .nodes import *

# This tells ComfyUI to look for a 'js' folder in our directory
WEB_DIRECTORY = "js"

# Tell ComfyUI about all the parts of our node
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS', 'WEB_DIRECTORY']