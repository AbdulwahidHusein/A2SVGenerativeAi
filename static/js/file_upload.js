
function fileSelect() {
    var fileInput = document.querySelector('.file-upload-input');
    var file = fileInput.files[0];
    var fileUploadContent = document.querySelector('.file-upload-content');
    fileUploadContent.style.display = 'block';
  
    if (file) {
      fileUploadContent.textContent = file.name;
    } else {
      fileUploadContent.textContent = '';
    }
  
    var fileInput = document.querySelector('.file-upload-input');
    var file = fileInput.files[0];
  
    if (file) {
      var fileSize = file.size / 1024 / 1024; // Convert to MB
      var fileExtension = file.name.split('.').pop().toLowerCase();
  
      if (fileSize <= 30 && (fileExtension === 'pdf' || fileExtension === 'docx' || fileExtension === 'txt')) {
        // Perform additional form validation if needed
  
        // Submit the form
        return true
      } else {
        return false
        }
    } else {
      return false
    }
  }
  