import os
import folder_paths

# --- The Node Class ---
class LoadTextFile:
    """
    A node that loads text from a file.
    It uses a custom widget to upload a .txt file.
    """
    
    @classmethod
    def INPUT_TYPES(s):
        return {
            "required": {
                # This string "image" MUST match the name in the
                # FormData.append("image", file) in the JS.
                # It tells ComfyUI to use our new "TEXTUPLOAD" widget.
                "image": ("TEXTUPLOAD", ) 
            }
        }

    # What the node will output
    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("text",)

    # The function that runs when the node is executed
    FUNCTION = "load_text"

    # The category in the right-click menu
    CATEGORY = "Rathius_ComfyNodes/Utils"
    
    # We don't want this node to run on file load, only when queued
    def IS_CHANGED(self, **kwargs):
        return float("inf")

    def load_text(self, image):
        # 'image' is the filename (e.g., "my_prompt.txt")
        # The widget has already uploaded it to the 'input' folder.
        file_path = os.path.join(folder_paths.get_input_directory(), image)
        
        try:
            # Open and read the file
            with open(file_path, 'r', encoding='utf-8') as f:
                text_content = f.read()
            
            # Return the text content as a tuple
            return (text_content, )
            
        except Exception as e:
            print(f"[LoadTextFile] Error: {e}")
            return (f"Error loading file: {e}", )

# --- Node Registration ---
NODE_CLASS_MAPPINGS = {
    "LoadTextFile_Rathius": LoadTextFile
}

# I updated the display name to reflect its new function
NODE_DISPLAY_NAME_MAPPINGS = {
    "LoadTextFile_Rathius": "Load Text from File (Upload)"
}