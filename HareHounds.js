$(function (){
	var prevClick;
	var solns;
	var move;
	var user_move = [0, 0];
	var curr_board = '0,0,1,3,10,0';
	var toggleTutor = false;
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
	//var board_list=['0','0','1','3','10','0'];	
	$("#tutor").click(function(){
		toggleTutor = !toggleTutor;
		if (toggleTutor==false){
			$('.square').removeClass("btn-danger btn-warning btn-success");
		}
	})
	$(document).on('click', '.open', function() {
		user_move[1] = parseInt($(this).attr('id'));
		getMove()
		curr_board = solns.filter(function(i){
			return JSON.stringify(user_move) === JSON.stringify(i['move'])
		});
		curr_board = curr_board[0]['board'].toString();
		list_to_board(string_to_list_board(curr_board));
		doComputerMove();
	});

	$(document).on('click', '.occupied-hound', function() {
		var this_id = $(this).attr('id');
		var next_moves = possibleMoves(parseInt(this_id));
		console.log(next_moves);
		for (id in next_moves){
			if (toggleTutor){
				labelVal(parseInt(this_id));
			}
			else {
				toggleClasses(makeId(next_moves[id]), "btn-outline-primary open", "btn-outline-dark");
			}
		}
		user_move[0] = parseInt(this_id);
		getMove();
		$('.occupied-hound').addClass('selected');
		prevClick = this;
	});

	$(document).on('click', '.selected', function(){
		list_to_board(string_to_list_board(curr_board));
	})
	function doComputerMove(){
		getMove();
		curr_board = move.toString();
		list_to_board(string_to_list_board(curr_board));
	}
	function getMove(){
		$.ajax({
			type: "GET",
			url: 'http://localhost:8000/?',
			dataType: 'json',
			data: {pos: curr_board},
			async: false,
		}).done(function (resp) {
			solns = resp;
			move = filterRemote(filterValue(resp))['board'];
		});
	}
	function list_to_board(board_list){
		toggleClasses('.square','empty btn-outline-dark' ,'occupied-hound selected open occupied-hare .btn-outline-primary')
		var hounds = [board_list[1], board_list[2], board_list[3]];
		for (i in hounds){
			toggleClasses(makeId(hounds[i]), 'occupied-hound','empty open');
		}
		toggleClasses(makeId(board_list[4]), 'occupied-hare', 'empty open');
	}
	function toggleClasses(button, add, remove){
		$(button).addClass(add);
		$(button).removeClass(remove);
	}

	function string_to_list_board(board_string){
		return board_string.split(',');
	}
	function makeId(num){
		return "#" + String(num);
	}
	function possibleMoves(location){
		getMove();
		var move_list = [];
		for (var i in solns){
			if (solns[i]['move'][0]===location){
				move_list.push(solns[i]['move'][1]);
			}
		}
		return move_list;
	}
	function labelVal(location){
		getMove();
		var next = possibleMoves(location);
		for (var i in next){
			var right_move = [location, next[i]];
			for (var j in solns){
				if (JSON.stringify(right_move) === JSON.stringify(solns[j]['move']) && solns[j]['value']===2){
					toggleClasses(makeId(next[i]), 'btn-danger open', 'btn-outline-dark');
				}
				else if (JSON.stringify(right_move) === JSON.stringify(solns[j]['move'])) {
					toggleClasses(makeId(next[i]), 'btn-success open', 'btn-outline-dark');
				}
			}
		}
	}

});

function filterRemote(filtered){
	var val = filtered[0]['value']
	var remotes = [];
	for (var i in filtered){
		remotes.push(filtered[i]['remoteness'])
	}
	if (val === 2){
		var minMax = Math.min.apply(Math, remotes)
	} else {
		var minMax = Math.max.apply(Math, remotes)
	}

	filtered = filtered.filter(function (i){
			return i['remoteness'] == minMax
		})
	random = Math.floor(Math.random()*filtered.length)
	return filtered[random];
}

function filterValue(solns){
	soln_win = solns.filter(function (i){
		return i['value'] != 2
	});
	if (soln_win.length != 0){
		solns = soln_win
	}
	return solns

}