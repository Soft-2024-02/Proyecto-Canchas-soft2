function previewImage(event) {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function () {
            document.getElementById('profileImagePreview').src = reader.result;
        };
        reader.readAsDataURL(file);
    }
}
function resetImage() {
    const defaultImage = "https://imgur.com/CuXg45K.jpg";
    document.getElementById('profileImagePreview').src = defaultImage;
    document.getElementById('profileImageInput').value = "";
}