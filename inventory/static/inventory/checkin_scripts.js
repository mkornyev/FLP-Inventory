$(document).ready(function() {

  // -------------- NOTES SCRIPTS: --------------
  var LOCAL_STORAGE_NOTES = 'notes-checkin-field'

  var notesFieldValue = localStorage.getItem(LOCAL_STORAGE_NOTES)
  if (notesFieldValue) {
    $('#id_checkin_notes').val(notesFieldValue)
    $('#notesCollapse').addClass('show') // show field
    toggleNotesButton()
  } 

  // Save Notes on AddItem / CreateFamily
  $('#addToCart-btn, #createItem-btn, .save-notes-on-click').on('click', function(){
    localStorage.setItem(LOCAL_STORAGE_NOTES, $('#id_checkin_notes').val())
  })
  $('#addNotes-btn').on('click', function(){
    toggleNotesButton()
  })

  function toggleNotesButton() {
    var btnHtml = $('#addNotes-btn').html()

    if(btnHtml.includes('Clear Notes')){
      localStorage.removeItem(LOCAL_STORAGE_NOTES)
      $('#id_checkin_notes').val('')

      $('#addNotes-btn')
      .html('Add Notes &#x270E;')
      .removeClass('btn-danger')
      .addClass('btn-warning')
    } else {
      $('#addNotes-btn')
      .html('Clear Notes &#x2715')
      .removeClass('btn-warning')
      .addClass('btn-danger')
    }
  }

  // Clear notes on Checkin
  $('#checkin-btn').on('click', function(){
    localStorage.removeItem(LOCAL_STORAGE_NOTES)
  })
});
