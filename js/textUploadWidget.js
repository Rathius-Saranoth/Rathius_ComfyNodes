import { app } from "../../scripts/app.js";

// This is the "correct" way to add frontend logic
app.registerExtension({
	name: "Rathius.TextUploader", // Unique name for our extension

	async beforeRegisterNodeDef(nodeType, nodeData, app) {
		// This runs for every node *before* it's added

		// Check if this is our node by its Python class name
		if (nodeData.name === "LoadTextFile_Rathius") {

			// This function will be called *after* the node is created on the canvas
			const onNodeCreated = nodeType.prototype.onNodeCreated;
			nodeType.prototype.onNodeCreated = function () {
				onNodeCreated?.apply(this, arguments);

				// Find the default "file_name" widget we created in Python
				const widget = this.widgets.find((w) => w.name === "file_name");

				// Create the "Choose File" button
				const fileInput = document.createElement("input");
				fileInput.type = "file";
				fileInput.accept = "text/plain,.txt";
				fileInput.style.display = "none";

				// Create the button widget
				const uploadButton = this.addWidget("button", "Choose .txt File", "None", () => {
					fileInput.click(); // Open the file picker when clicked
				});
				uploadButton.serialize = false; // Don't save this button's value in workflows

				// Handle what happens when a file is selected
				fileInput.addEventListener("change", (event) => {
					if (fileInput.files.length) {
						uploadFile(fileInput.files[0]);
					}
				});

				// Create the upload function
				const uploadFile = async (file) => {
					const body = new FormData();

					// 'input' is the default folder, but we can specify a subfolder
					body.append("subfolder", "text_prompts");
					body.append("overwrite", "true"); // Overwrite existing files
					// The server's /upload/image endpoint handles *any* file
					body.append("image", file, file.name);

					uploadButton.name = "Uploading...";

					try {
						// Send the file to the server
						const response = await fetch("/upload/image", {
							method: "POST",
							body: body,
						});

						if (response.status === 200) {
							const data = await response.json();
							// Set the value of the *original* (hidden) widget
							// This is what Python will receive
							let filePath = data.name;
							if (data.subfolder) {
								filePath = data.subfolder + "/" + filePath;
							}

							filePath = filePath.replace(/\\/g, "/"); // e.g., "text_prompts/my_prompt.txt"
							widget.value = filePath;

							// Truncate for display if too long
							let displayName = filePath;
							if (displayName.length > 30) {
								displayName = displayName.substring(0, 20) + "..." + displayName.substring(displayName.length - 10);
							}

							uploadButton.name = `Loaded: ${displayName}`;
						} else {
							alert(response.status + " - " + response.statusText);
							uploadButton.name = "Choose .txt File";
						}
					} catch (error) {
						alert(error);
						uploadButton.name = "Choose .txt File";
					}
				};

				// Add the hidden file input to the document
				document.body.appendChild(fileInput);

				// Hide the original string widget
				widget.type = "hidden"; // We don't want to see the text box
				widget.serialize = true; // We *do* want to save its value
			};
		}
	},
});