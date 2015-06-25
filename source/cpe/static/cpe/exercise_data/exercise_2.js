var into_numbers = function(str) {
	var arr = str.trim().split(/[\s,]+/);
	for (var i = 0 ; i < arr.length ; i++) arr[i] = parseInt(arr[i]);
	return arr;
}

var draw_array = function (panel, array, correct_values) {
	for (var i = 0 ; i < array.length ; i++) {
		var cell = $("<span>").text(array[i]).addClass("array_cell");
		if (correct_values != undefined && correct_values[i] != undefined) {
			cell.text(array[i] + " / " + correct_values[i]);
			cell.addClass("array_cell_wrong");
		}
		panel.append(cell);
	}
}

var visualize_input = function(panel, verdict_details, checker_comment) {
	if (checker_comment) {
		console.assert(checker_comment.checker_id == 1);
		
		if (checker_comment.input) {
			draw_array(panel, checker_comment.input);
		} else {
			panel.text("Some array of size " + checker_comment.input_size);
		}
	} else {
		var input = into_numbers(verdict_details.input);
		if (input[0] == 1) {
			var input = input.splice(2, input[1]);
			draw_array(panel, input);
		} else {
			panel.text("Some array");
		}
	}
};

var visualize_result = function(panel, verdict_details, checker_comment) {
	if (checker_comment) {
		console.assert(checker_comment.checker_id == 1);
		
		if (checker_comment.actual) {
			while (checker_comment.actual.length < checker_comment.expected.length)
				checker_comment.actual[checker_comment.actual.length] = "-";
			var errors = { };
			for (var i = 0 ;  i < checker_comment.expected.length ; i++)
				if (checker_comment.actual[i] != checker_comment.expected[i]) errors[i] = checker_comment.expected[i];
			for (var i = checker_comment.expected.length ; i < checker_comment.actual.length ; i++)
				errors[i] = "-";
			draw_array(panel, checker_comment.actual, errors);
		}
	}
}

var draw_array = function (panel, array, correct_values) {
	for (var i = 0 ; i < array.length ; i++) {
		var cell = $("<span>").text(array[i]).addClass("array_cell");
		if (correct_values != undefined && correct_values[i] != undefined) {
			cell.text(array[i] + " / " + correct_values[i]);
			cell.addClass("array_cell_wrong");
		}
		panel.append(cell);
	}
}

var show_input2 = function(panel, input) {
	var array = into_numbers(input);
	var n = array[1];	
	array = array.splice(2, n);
	
	draw_array(panel, array);
};

var show_result2 = function(panel, verdict_details) {
	window.res = verdict_details;
	
	return;
	var verdict = JSON.parse(verdict_details);
	var n = output[0];
	var output_array = output.splice(1, n);
	
	var expected_output = into_numbers(verdict_details.answer);
	var n2 = expected_output[0];
	var expected_output_array = expected_output.splice(1, n2);
	var correct_values = { };
	
	for (var i = 1 ; i < n2 ; i++) if (output_array[i] != expected_output_array[i]) correct_values[i] = expected_output_array[i];
	
	draw_array(panel, output_array, correct_values);
}