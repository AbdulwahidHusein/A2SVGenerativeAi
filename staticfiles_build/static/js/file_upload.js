
function fileSelect() {
    var fileInput = document.querySelector('.file-upload-input');
    var file = fileInput.files[0];
  
    if (file) {
      var fileSize = file.size / 1024 / 1024; // Convert to MB
      var fileExtension = file.name.split('.').pop().toLowerCase();
      if (fileExtension !== 'pdf'){
        return "only pdf files are allowed"
      }
      if (fileSize <= 20 && (fileExtension === 'pdf' || fileExtension === 'docx')) {
        return true
      } else {
        return "file size should be less than 20mb"
        }
    } else {
      return "please select a file"
    }
  }
  