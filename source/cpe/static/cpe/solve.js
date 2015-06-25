var load_status_interval;

var show_input = function(callback_result, verdict_details, checker_comment) {
	$("#input_panel").show();
	visualize_input($("#input_panel_body"), verdict_details, checker_comment);
};

var show_result = function(callback_result, verdict_details, checker_comment) {
	$("#result_panel").show();
	visualize_result($("#result_panel_body"), verdict_details, checker_comment);
};

var verdict_formatters = {
	IP: function(panel) {
		panel.text("Attempt is being checked...");
	},
	CE: function(verdict_panel, result) {
		verdict_panel.text("Code didn't compile. Compilation error:");
		verdict_panel.append("<br>");
		verdict_panel.append(result.verdict_details.compilation_error.replace("\n", "<br>"));
	},
	AC: function(verdict_panel) {
		verdict_panel.text("Congratulations! Your code is gorgeous!");
	},
	TL: function(verdict_panel, result, verdict_details) {
		verdict_panel.text("Your code was too slow, any idea how to make it faster?");
		show_input(result, verdict_details);
	},
	ML: function(verdict_panel, result, verdict_details) {
		verdict_panel.text("Your solution consumed too much memory, which is no good");
		show_input(result, verdict_details);
	},
	RE: function(verdict_panel, result, verdict_details) {
		verdict_panel.text("Your solution had a runtime error while solving one of the test cases");
		show_input(result, verdict_details);
	},
	WA: function(verdict_panel, result, verdict_details, checker_comment) {
		verdict_panel.text("Your solution wasn't absolutely correct, look for bugs");
		show_input(result, verdict_details, checker_comment);
		show_result(result, verdict_details, checker_comment);
	},
};

function check_status() {
	$.get("/update-status/" + attempt_id, function(res) {
		res = JSON.parse(res);
		var verdict_details = res.verdict_details;
		var checker_comment = verdict_details && verdict_details.hasOwnProperty('checker_comment') ? JSON.parse(verdict_details.checker_comment) : undefined;
		console.log(res);
		
		verdict_formatters[res.verdict_code]($("#verdict_panel_body"), res, verdict_details, checker_comment);
		if (!res.is_in_progress) {
			clearInterval(load_status_interval);
		}
	});
}

$(function (){
	$("#verdict_panel").hide();
	$("#input_panel").hide();
	$("#result_panel").hide();
	if (attempt_id !== null) {
		$("#verdict_panel").show();
		$("#verdict_panel_body").text("Loading attempt result...");

		load_status_interval = window.setInterval(check_status, 1000);
	}
});
