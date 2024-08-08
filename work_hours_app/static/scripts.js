function setMonthAndSubmit(month) {
    document.getElementById('selectedMonth').value = month; // Set the hidden input value
    document.forms[0].submit(); // Submit the form
}