function onInputBoxUpdate() {
    let inputBox = document.getElementById('input-box');
    value = inputBox.value.toString();

    // Make sure the input box (which contains the name of the crypto to monitor) contains 5 characters or less.
    if(value.length > 5)
    {
        value = value.substring(0, 5);
    }

    inputBox.value = value.toUpperCase();
}
