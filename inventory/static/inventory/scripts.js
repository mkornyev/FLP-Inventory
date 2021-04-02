
$(document).ready(function() {

  // For Bootstrap Tooltips: https://getbootstrap.com/docs/5.0/components/tooltips/
  var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))

  var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
    return new bootstrap.Tooltip(tooltipTriggerEl)
  })

})