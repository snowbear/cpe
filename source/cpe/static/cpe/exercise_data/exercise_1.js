var into_numbers = function(s) {
	s = s.replace('\n', ' ').replace('\r', "");
	
	var array = s.split(' ');
	for (var i = 0 ; i < array.length ; i++) array[i] = parseInt(array[i]);	
	return array;
}

var visualize_input = function(panel, verdict_details, checker_comment) {
	if (checker_comment) {
		console.assert(checker_comment.checker_id == 1);
		panel.text(checker_comment.input);
	} else {
		var array = into_numbers(verdict_details.input);
		console.log(array);
		if (array[0] == 1) panel.text(array[1]);
		else panel.text("Unknown input");
	}
};

var visualize_result = function(panel, verdict_details, checker_comment) {
	console.assert(checker_comment.checker_id == 1);
	panel.text(checker_comment.actual + " / " + checker_comment.expected);
}