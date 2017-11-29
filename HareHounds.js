$(function (){
	var prevClick;
	var edges = {
	    0: ["#1", "#2", "#3"],
	    1: ["#0", "#2", "#4", "#5"],
	    2: ["#0", "#1", "#3", "#5"],
	    3: ["#0", "#2", "#5", "#6"],
	    4: ["#1", "#5", "#7"],
	    5: ["#1", "#2", "#3", "#4", "#6", "#7", "#8", "#9"],
	    6: ["#3", "#5", "#9"],
	    7: ["#4", "#5", "#8", "#10"],
	    8: ["#5", "#7", "#9", "#10"],
	    9: ["#5", "#6", "#8", "#10"],
	    10:["#7", "#8", "#9"]
	};
	var curr_board;
	$(document).on('click', '.open', function() {
		toggleClasses(prevClick, "empty", "occupied-hound selected");
		toggleClasses(".empty", "btn-outline-dark", "btn-outline-primary open");
		toggleClasses(this, "occupied-hound", "empty open");
	});

	$(document).on('click', '.occupied-hound', function() {
		var this_id = $(this).attr('id');
		var moves = edges[this_id];
		for (id in moves){
			var id_num = $(moves[id]).attr('id');
			if ($(moves[id]).hasClass("empty") &&
				(Math.floor((this_id - 1)/ 3) <= Math.floor((id_num - 1) / 3))){
						toggleClasses(moves[id], "btn-outline-primary open", "btn-outline-dark");
					}
			}
		$('.occupied-hound').addClass('selected');
		prevClick = this;
	});

	$(document).on('click', '.selected', function(){
		toggleClasses(".open", "btn-outline-dark", "btn-outline-primary open");
		toggleClasses('.selected', 'occupied-hound', 'selected');
	})
	$(".occupied-hare").button({
		icons: {primary: null},
	    text: false
	}).addClass("hare");
	function doComputerMove(){

	}
	function toggleClasses(button, add, remove){
		$(button).addClass(add);
		$(button).removeClass(remove);
	}

})