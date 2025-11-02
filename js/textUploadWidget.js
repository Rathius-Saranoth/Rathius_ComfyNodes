import { app } from "../../../scripts/app.js";

// This file just needs to register the new widget type
function textUploadWidget(node, inputName, inputData, app) {
	const widget = {
		type: inputData[0], // "TEXTUPLOAD"
		name: inputName,
		size: [128, 88], // Widget size
		draw(ctx, node, width, y) {}, // No need to draw anything
		computeSize(...args) {
			return [128, 88]; // Match the size
		},
		async serializeValue(nodeId, widgetIndex) {
			return node.widgets[widgetIndex].value;
		},
	};

	// Create the "Choose File" button
	const fileInput = document.createElement("input");
	fileInput.type = "file";
	fileInput.accept = "text/plain,.txt"; // <--- This is the important change
	fileInput.style.display = "none";

	// Handle file selection
	fileInput.addEventListener("change", (event) => {
		if (fileInput.files.length) {
			uploadFile(fileInput.files[0]);
		}
	});

	// Create the button that opens the file picker
	const uploadButton = document.createElement("button");
	uploadButton.type = "button";
	uploadButton.innerText = "Choose .txt File to Upload";
	uploadButton.className = "comfy-btn";
	uploadButton.style.width = "100%"; // Make button fill widget
	uploadButton.style.marginTop = "10px";
	uploadButton.addEventListener("click", () => {
		fileInput.click();
	});

	// Function to handle the upload
	async function uploadFile(file) {
		const body = new FormData();
		// We use "image" to match the server's /upload/image endpoint
		// The server doesn't care about the file type, just saves it.
		body.append("image", file); 
		body.append("overwrite", "true");
		widget.value = file.name; // Store the filename for the backend

		uploadButton.innerText = "Uploading...";
		
		try {
			const response = await fetch("/upload/image", {
				method: "POST",
				body: body,
			});

			if (response.status === 200) {
				uploadButton.innerText = file.name; // Show the new filename
				node.setValue(file.name); // Set the node's internal value
			} else {
				alert(response.status + " - " + response.statusText);
				uploadButton.innerText = "Choose .txt File to Upload";
			}
		} catch (error) {
			alert(error);
			uploadButton.innerText = "Choose .txt File to Upload";
		}
	}

	// Add the button to the node's widget area
	node.addDOMWidget(inputName, "button", uploadButton, widget);
	document.body.appendChild(fileInput); // Add the hidden file input

	// Handle drag and drop
	node.onDragOver = function (e) {
		if (e.dataTransfer.items.length > 0) {
			const item = e.dataTransfer.items[0];
			// Allow .txt files (which often have no MIME type) or text/plain
			return item.kind === 'file' && (item.type === "text/plain" || item.type === "");
		}
		return false;
	};

	node.onDragDrop = function (e) {
		let handled = false;
		for (const file of e.dataTransfer.files) {
			if (file.type === "text/plain" || file.name.endsWith(".txt")) {
				uploadFile(file);
				handled = true;
			}
		}
		return handled;
	};

	return widget;
}

// Register our new "TEXTUPLOAD" widget with ComfyUI
app.registerWidgetType("TEXTUPLOAD", textUploadWidget);