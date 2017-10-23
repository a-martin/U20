/**
 * Randomize array element order in-place.
 * Using Fisher-Yates shuffle algorithm.
 * (from http://stackoverflow.com/questions/2450954/how-to-randomize-a-javascript-array)
 */
function shuffleArray(array) {
    for (var i = array.length - 1; i > 0; i--) {
        var j = Math.floor(Math.random() * (i + 1));
        var temp = array[i];
        array[i] = array[j];
        array[j] = temp;
    }
    return array;
}

/**
 * Insert value into form key
 * (from psiTurk)
 */
function insert_hidden_into_form(formName, name, value ) {
	var hiddenField = document.createElement('input');
	hiddenField.setAttribute('type', 'hidden');
	hiddenField.setAttribute('name', name);
	hiddenField.setAttribute('value', value );
	$('#'+formName).append( hiddenField );
}
