$(document).ready(function() {

  // -------------- NOTES SCRIPTS: --------------

  var notesFieldValue = localStorage.getItem('notes-field')
  if (notesFieldValue) {
    $('#id_checkout_notes').val(notesFieldValue)
    $('#notesCollapse').addClass('show') // show field
    toggleNotesButton()
  } 

  // Save Notes on AddItem / CreateFamily
  $('#addToCart-btn, #createFam-btn, #createItem-btn, .save-notes-on-click').on('click', function(){
    localStorage.setItem('notes-field', $('#id_checkout_notes').val())
  })
  $('#addNotes-btn').on('click', function(){
    toggleNotesButton()
  })

  function toggleNotesButton() {
    var btnHtml = $('#addNotes-btn').html()

    if(btnHtml.includes('Clear Notes')){
      localStorage.removeItem('notes-field')
      $('#id_checkout_notes').val('')

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

  // Clear notes on Checkout
  $('#checkout-btn').on('click', function(){
    localStorage.removeItem('notes-field')
  })
});