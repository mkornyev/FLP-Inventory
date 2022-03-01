$(document).ready(function() {

  // -------------- NOTES SCRIPTS: --------------
  var LOCAL_STORAGE_NOTES = 'notes-checkout-field'

  // Replace notes field w/oldNotes if present
  var invalidCheckout = $('#fromInvalidCheckoutRedirect')
  if(invalidCheckout.length != 0){
    var oldNotes = localStorage.getItem('old-notes-field')
    localStorage.setItem(LOCAL_STORAGE_NOTES, oldNotes)
    localStorage.removeItem('old-notes-field')
  }

  var notesFieldValue = localStorage.getItem(LOCAL_STORAGE_NOTES)
  if (notesFieldValue) {
    $('#id_checkout_notes').val(notesFieldValue)
    $('#notesCollapse').addClass('show') // show field
    toggleNotesButton()
  } 

  // Save Notes on AddItem / CreateFamily
  $('#addToCart-btn, #createFam-btn, #createItem-btn, .save-notes-on-click').on('click', function(){
    localStorage.setItem(LOCAL_STORAGE_NOTES, $('#id_checkout_notes').val())
  })
  $('#addNotes-btn').on('click', function(){
    toggleNotesButton()
  })

  function toggleNotesButton() {
    var btnHtml = $('#addNotes-btn').html()

    if(btnHtml.includes('Clear Notes')){
      localStorage.removeItem(LOCAL_STORAGE_NOTES)
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
    var oldNotes = $('#id_checkout_notes').val()
    localStorage.removeItem(LOCAL_STORAGE_NOTES)
    localStorage.setItem('old-notes-field', oldNotes) // in case a Checkout validation fails 
  })

});

