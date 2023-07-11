function submitForm() {
  var submitBtn = document.getElementById('submitBtn');
  var loadingSpinner = document.getElementById('loadingSpinner');
  var myForm = document.getElementById('myForm');
  // Disable the submit button
  submitBtn.disabled = true;

  // Hide the submit button and show the loading spinner
  submitBtn.style.display = 'none';
  loadingSpinner.style.display = 'block';
  myForm.submit();
  // wait for 1 second after submitting the form before enabling the submit button
  setTimeout(function() {
    console.log('waiting 1 second')
  }, 1000);

  document.addEventListener('DOMContentLoaded', function() {
    // Page content is loaded, and the loading indicator may have been removed
    submitBtn.disabled = false;
    submitBtn.style.display = 'block';
    loadingSpinner.style.display = 'none';
  }); 
}