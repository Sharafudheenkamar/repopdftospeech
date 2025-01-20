function readURL(input) {
  if (input.files && input.files[0]) {

    var reader = new FileReader();
    var file = input.files[0];

    reader.onload = function(e) {
      $('.image-upload-wrap').hide();

      var fileType = file.type;
      var fileUrl = e.target.result;

      // Set file data to display
      $('.file-upload-image').attr('data', fileUrl); // Set the data attribute to display the file
      $('.file-upload-image').attr('type', fileType); // Set the type attribute based on the file's MIME type

      // For PDF files or non-image files, make sure it displays the file properly in the <object> tag
      if (fileType === 'application/pdf') {
        $('.file-upload-image').attr('data', fileUrl); // PDF is directly displayed in the object
        $('.file-upload-image').attr('type', 'application/pdf');
      } else if (fileType.startsWith('image/')) {
        $('.file-upload-image').attr('data', fileUrl); // For image files
        $('.file-upload-image').attr('type', fileType);
      } else {
        // Handle other file types
        $('.file-upload-image').attr('data', fileUrl);
        $('.file-upload-image').attr('type', fileType);  // This can be expanded to handle more types if needed
      }

      $('.file-upload-content').show();
      $('.image-title').html(file.name);
    };

    reader.readAsDataURL(file); // This loads the file data

  } else {
    removeUpload();
  }
}

function removeUpload() {
  $('.file-upload-input').replaceWith($('.file-upload-input').clone());
  $('.file-upload-content').hide();
  $('.image-upload-wrap').show();
}

$('.image-upload-wrap').bind('dragover', function () {
  $('.image-upload-wrap').addClass('image-dropping');
});

$('.image-upload-wrap').bind('dragleave', function () {
  $('.image-upload-wrap').removeClass('image-dropping');
});
