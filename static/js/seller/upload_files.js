const customFileInput = document.querySelector('.custom-file-input');
const fileInput = document.querySelector('#image_product');
customFileInput.addEventListener('click', () => {
    fileInput.click();
});

fileInput.addEventListener('change', () => {
    if (fileInput.files.length>1){
        const fileName = fileInput.files[0].name;
        customFileInput.textContent = fileName + "...";
    }
    else{
        const fileName = fileInput.files[0].name;
        customFileInput.textContent = fileName;
    }
});