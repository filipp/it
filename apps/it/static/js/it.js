$('.media').hover(
    function(){
      $(this).find('.btn-group').show();
    },
    function(){
      $('.btn-group').hide();
  });
  Dropzone.options.myAwesomeDropzone = {
    paramName: "attachment", // The name that will be used to transfer the file
    maxFilesize: 2, // MB
  };
  $('.confirm').click(function(e){
    if(confirm('Are you sure?')) {
      return true;
    }
    e.preventDefault();
  });
  $('.searchfield').on('keyup', function(e){
    if(e.keyCode == 13) {
      document.location = '/search/?q=' + $(this).val();
    }
  });
  $('.autocomplete').each(function(i, e){
    $(e).autocomplete({source: $(e).data('source')});
  });
  $('.draggable').draggable({opacity: 0.75, zIndex: 100, cursor: 'pointer'});
  $('.dragarea').droppable({
    out: function(e, ui) {
      $.ajax($(ui.draggable).data('destroy'));
      $(ui.draggable).remove();
    }
  });
