function updateUploadedImagesMessage(input) {
    const messageElement = document.getElementById("uploaded-images-message");
    const fileList = input.files;
    const imageNames = Array.from(fileList).map(file => file.name);
    messageElement.textContent = "Images selected: " + imageNames.join(", ");
}


const imageInput = document.getElementById("image_product");
imageInput.addEventListener("change", function() {
    updateUploadedImagesMessage(this);
});