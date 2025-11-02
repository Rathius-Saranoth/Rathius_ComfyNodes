import os
import folder_paths

# --- Get Text Files ---
# 1. Get the ComfyUI 'input' directory
input_dir = folder_paths.get_input_directory()

# 2. Find all .txt files in that directory
# We os.path.isfile to make sure we don't grab directories
text_files = [
    f for f in os.listdir(input_dir)
    if os.path.isfile(os.path.join(input_dir, f)) and f.endswith(".txt")
]

# --- The Node Class ---
class LoadTextFile:
    """
    A node that loads text from a file in the ComfyUI/input/ directory.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # This creates the dropdown widget with our file list
                "file_name": (text_files, )
            }
        }

    # What the node will output
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",) # Optional, but good practice

    # The function that runs when the node is executed
    FUNCTION = "load_text"

    # The category in the right-click menu
    CATEGORY = "Rathius_ComfyNodes/Utils"

    def load_text(self, file_name):
        # Get the full path to the file
        file_path = os.path.join(input_dir, file_name)
        
        try:
            # Open and read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # Nodes must return their outputs as a tuple
            return (text_content, )
            
        except Exception as e:
            print(f"[LoadTextFile] Error: {e}")
            # Return the error as a string so you can see it in ComfyUI
            return (f"Error loading file: {e}", )

# --- Node Registration ---
# This tells ComfyUI about our new node
NODE_CLASS_MAPPINGS = {
    "LoadTextFile_Rathius": LoadTextFile
}

# This sets the name that appears in the Add Node menu
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadTextFile_Rathius": "Load Text from File"
}