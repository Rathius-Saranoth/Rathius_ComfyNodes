# Required boilerplate for ComfyUI custom nodes.
# - class LoadTextFile: - "Hello, I am a new node."
# - INPUT_TYPES - "Here is the form for the inputs I need."
# - RETURN_TYPES - "Here is what I will give back."
# - FUNCTION - "This is the name of the function that does the actual work."
# - CATEGORY - "Put me in this menu, please."
# - load_text(self, ...) - "I am the actual function that does the work."
# - NODE_CLASS_MAPPINGS - "This is the official registration form."

# Import any necessary modules
import os
import folder_paths
import hashlib

# Here you are naming your node class
class LoadTextFile_Rathius:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # This is just a placeholder text box. 
                # Our JS will find this widget by its name ("file_name") 
                # and replace it with an upload button.
                "file_name": ("STRING", {"default": "example.txt", "multiline": False}),
            }
        }
    
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)
    FUNCTION = "load_text"
    CATEGORY = "RathiusNodes/Utils"

    @classmethod
    def IS_CHANGED(cls, file_name):
        # This re-runs the node if the file name changes
        try:
            file_path = folder_paths.get_annotated_filepath(file_name)
        except:
            # File doesnt exist yet
            return float("inf")
        
        m = hashlib.sha256()
        with open(file_path, 'rb') as f:
            m.update(f.read())
        return m.digest().hex()
    
    def load_text(self, file_name):
        # This function is more robust. It searches in all known input folders.
        try:
            file_path = folder_paths.get_annotated_filepath(file_name)
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            return (text_content, )
        except Exception as e:
            print(f"[LoadTextFile] Error: {e}")
            # Return the error message as a string so it can be debugged
            return (f"Error: {e}", )

# --- Node Registration ---
NODE_CLASS_MAPPINGS = {
    "LoadTextFile_Rathius": LoadTextFile_Rathius
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadTextFile_Rathius": "Load Text from File (Upload)"
}