$(document).ready(function() {  

  var currInputs = [] // All the 'open' inputs
  var EDIT_IN_PLACE_CLASSNAME = 'edit-in-place'
  var INPUT_WIDTH = '85px'
  var UPDATED_COLOR = '#095cb5'

  $('td.' + EDIT_IN_PLACE_CLASSNAME).css('cursor', 'pointer')
  $('td.' + EDIT_IN_PLACE_CLASSNAME).on('click', replaceWithInput)    
  $(window).on('click', closeAllOpenInputs)
  $(window).on('keypress', checkEnter) // Prevent ENTER from submitting form (when filling out price)

  function replaceWithInput(){
    var input = document.createElement('input')
    input.id = this.id // id = "#-price"
    input.value = $(this).text()
    input.type = 'number'
    input.step = "0.01"
    input.style.width = INPUT_WIDTH
    input.className = 'form-control'

    this.parentNode.replaceChild(input, this)
    currInputs.push(input)
  }

  function closeAllOpenInputs(evt){
    if(!(evt.target.classList.value == EDIT_IN_PLACE_CLASSNAME || evt.target.classList.value == 'form-control')){
      currInputs.forEach(function(i){
        // Inject new element 
        var td = document.createElement('td')
        td.id = i.id
        td.className = EDIT_IN_PLACE_CLASSNAME
        td.innerText = i.value
        td.onclick = replaceWithInput
        td.style.color = UPDATED_COLOR
        td.style.fontWeight = '800'

        i.parentNode.replaceChild(td, i)

        // Update Tot Value 
        var firstHyphen = i.id.indexOf('-');
        var itemId = i.id.substring(0, firstHyphen);
        var secondHyphen = i.id.indexOf('-', firstHyphen + 1);
        var is_new = i.id.substring(firstHyphen + 1, secondHyphen)
        var quantity = $('#'+itemId+'-'+is_new+'-quantity').first().text()
        var newValue = (parseFloat(quantity) * parseFloat(i.value)).toFixed(2)
        var oldValue = $('#'+itemId+'-'+is_new+'-value').text()
        $('#'+itemId+'-'+is_new+'-value').text(newValue).css('color', UPDATED_COLOR).css('font-weight', '800')

        var oldStrTotal = $('#report_total').text()
        var oldNumTotal = parseFloat(oldStrTotal.substring(oldStrTotal.indexOf('$')+1, oldStrTotal.length))
        var newNumTotal = oldNumTotal + parseFloat(newValue) - parseFloat(oldValue)
        $('#report_total').text('$'+newNumTotal.toFixed(2))
        console.log(i.id)
        console.log(is_new)
        console.log('#'+itemId+'-'+is_new+'-adjustment')

        // Update Hidden Input
        $('#'+itemId+'-'+is_new+'-adjustment').attr('value', i.value)
      })
      currInputs = []
    }
  }

  function checkEnter(e){
    var txtArea = /textarea/i.test((e.target || e.srcElement).tagName);
    return txtArea || (e.keyCode || e.which || e.charCode || 0) !== 13;
  }
})