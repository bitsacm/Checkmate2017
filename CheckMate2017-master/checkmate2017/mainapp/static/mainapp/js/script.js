// add id = player_girl to girl's g tag
$(document).ready(function(){

	// developer_info
	$('body').prepend('<div id="dev_info"><span></span></div>');
	

	// names on buildings
	$('body').append('<div id="building_names"></div>');
	// $('#building_names').css({'position': 'absolute','top': 0, 'left':0, 'width': 'fit-content', 'background': 'rgba(0,0,0,0.2)', 'color': '#eee', 'fontSize': '10px', 'padding': '2px', 'borderRadius': '6px'});


	//fancy colors
	$('body').css('backgroundColor', 'rgba(210, 186, 2, 0.14)');
	$('body').css('fontFamily', 'arial, verdana');
	
	var svg = $('svg');
	
	// getNamedItem('viewbox').value
	
	var player = getPlayer();

	player.fadeIn();
	window.playground = svg;

	function getPlayer(){
		$('#player_boy').hide();
		$('#player_girl').hide()

		// ...?
		return $('#player_girl');
	}



	/*****
	*
	*  Walking on the road
	*
	******/


	var roads = $('*[data-name=road]');
	
	var inital_pos = [-1060, 250]
	// initial position
	TweenMax.set(player, {scale: .5, xPercent: -1060, yPercent: 250})
	
	// player properties 
	var player_props = {
		rel_x: -1060,
		rel_y: 250,
		step: 10,
		top: 0,
		left:0,
		width: player[0].getBoundingClientRect().width,
		rect: player[0].getBoundingClientRect(),
		new_rect: {}
	}
	// console.log(player[0].getBoundingClientRect())
	var relative_x = player_props.rel_x;
	var relative_y = player_props.rel_y;

	var viewport_coords = {
		x: 0,
		y: 0,
		prev_x:0,
		prev_y: 0
	}
	

	update_viewPort_coords(1)
	
	// movement
	$(document).keydown(function(e){
		player_props.top = 0;
		player_props.left = 0;
		// console.log(e.keyCode);
		if((e.keyCode>40 || e.keyCode<37 ) && e.keyCode!=32)return;
		else if(e.keyCode == 38){
			player_props.top = -(player_props.step);
		}else if(e.keyCode == 40){
			player_props.top = player_props.step;
		}else if(e.keyCode==39){
			player_props.left = player_props.step;
		}else if(e.keyCode == 37){
			player_props.left = -(player_props.step);
		}else if(e.keyCode == 32){
			return window.lightbox();
		}
		// player_props.rect = player[0].getBoundingClientRect();
		// move();
		// render(player_props.top,player_props.left);
	})
	
	var prev_road = null;
	var history = [inital_pos, inital_pos,inital_pos, inital_pos,inital_pos];
	var states = [true, true, true, true, true];

	function move(player_props){
		var inRoad = false;
		var notInCircle = false;
		for(i in player_props.rect){
			player_props.new_rect[i] = player_props.rect[i]; 
		}

		var move = player_props.top || player_props.left;
		if(!move){
			return;
		}

		player_props.new_rect.top += player_props.top;
		player_props.new_rect.bottom -= player_props.top;
		player_props.new_rect.left += player_props.left;
		player_props.new_rect.right -= player_props.left;
		// console.log(player_props.new_rect)

		if(prev_road){
			inRoad = checkEnclosed(player_props.new_rect, prev_road)
		}
		console.log(inRoad)

		if(!inRoad){
			roads.each(function(ind, ele){
					if(checkEnclosed(player_props.new_rect, ele)){
						inRoad = true;
						prev_road = ele;
						console.log(ele);
					}
			})
		}

		notInCircle = checkNotAboutToBeEnclosed(player_props.new_rect, $('#gandhi_circle')[0]) && checkNotAboutToBeEnclosed(player_props.new_rect, $('#patel_circle')[0]);
		
		// console.log(inRoad, notInCircle);
		var state = (inRoad && notInCircle);
		states.push(state);
		console.log(state)
				
		if(state && move){
			player_props.rel_x +=  player_props.left;
			player_props.rel_y +=  player_props.top;
			render(player_props);
		}else{
			console.log('bounce');
			[[player_props.rel_x, player_props.rel_y]] = history.slice(-5, -4);
			render(player_props);
		}


	}

	// storing each state
	


	// render animation
	function render(player_props){
		
		
	
		TweenMax.to(player, .4,{xPercent:(player_props.rel_x ), yPercent:(player_props.rel_y)});

		relative_y = player_props.rel_y;
		relative_x = player_props.rel_x;

		
		history.push([player_props.rel_x, player_props.rel_y])

	}

	function checkStuck(states){
		return (states.indexOf(true) == -1);
	}

	function update_viewPort_coords(init){
		// console.log('called')
		var player_rect = player[0].getBoundingClientRect();
		var parent_rect = $('#rect2261')[0].getBoundingClientRect();
		viewport_coords.x = player_rect.left - parent_rect.left - $(window).width()/2 ;
		viewport_coords.y = player_rect.top - parent_rect.top - $(window).height()/2 ;
		
		// boundary conditions
		// console.log(parent_rect.top + viewport_coords.y - viewport_coords.prev_y > 0)
		// console.log(parent_rect.top, viewport_coords.y - viewport_coords.prev_y)
		if(parent_rect.top - viewport_coords.y + viewport_coords.prev_y > 0){
			// console.log(viewport_coords.y)
			viewport_coords.y = viewport_coords.prev_y + parent_rect.top;
			// console.log(viewport_coords.y)
		}
		else if(parent_rect.bottom - viewport_coords.y + viewport_coords.prev_y < $(window).height()){
			// console.log('called', parent_rect)
			viewport_coords.y = - $(window).height() + viewport_coords.prev_y + parent_rect.bottom;
		}

		if(parent_rect.left - viewport_coords.x + viewport_coords.prev_x > 0){
			// console.log(viewport_coords.y)
			viewport_coords.x = viewport_coords.prev_x + parent_rect.left;
			// console.log(viewport_coords.y)
		}
		else if(parent_rect.right - viewport_coords.x + viewport_coords.prev_x < $(window).width()){
			// console.log('called', parent_rect)
			viewport_coords.x = - $(window).width() + viewport_coords.prev_x + parent_rect.right;
		}


		
		if(init){

			viewport_coords.prev_x = viewport_coords.x;
			viewport_coords.prev_y = viewport_coords.y

			svg[0].attributes.getNamedItem("viewBox").value = ( viewport_coords.prev_x+ " " + viewport_coords.prev_y + " " + $(window).width()+ " "+ $(window).height());
		}
		else{
			TweenMax.to(viewport_coords,3, {
		      prev_x: viewport_coords.x,
		 	  prev_y: viewport_coords.y, 
			  onUpdate: function () {
			    svg[0].attributes.getNamedItem("viewBox").value = ( viewport_coords.prev_x+ " " + viewport_coords.prev_y + " " + $(window).width()+ " "+ $(window).height());
			  },
			  ease:Power0.easeNone,
			});
		}

	}

	var view = setInterval(function(){
		update_viewPort_coords(0);
	}, 1000)

	// returns true if  enclosing
	function checkEnclosed(player_rect, container){
		// var player_rect = player.getBoundingClientRect();
		var container_rect = container.getBoundingClientRect();

		// boundary checking
		return checkBoundary(player_rect, container_rect);
	}

	function checkBoundary(player_rect, container_rect){
		var cond_right = ((player_rect.right) >(container_rect.left ) && (player_rect.right ) < container_rect.right),
		cond_left = 	((player_rect.left) > container_rect.left && (player_rect.left) < container_rect.right),
		cond_top = 	((player_rect.top)> container_rect.top) && ((player_rect.top) < container_rect.bottom),
		cond_bottom = ((player_rect.bottom ) > container_rect.top) && ((player_rect.bottom )< container_rect.bottom);
	
		return (cond_right && cond_left && cond_top && cond_bottom)
	}

	//hardest part : naming the function
	function checkNotAboutToBeEnclosed(player_rect, container){
		// var player_rect = player.getBoundingClient	Rect();
		var container_rect = container.getBoundingClientRect();
		var mutable_rect = {};

		for(i in container_rect){
			mutable_rect[i] = container_rect[i]; //because container_rect is frozen by default :O !
		}

		var neigbourhood = 0;
		
		mutable_rect.left = container_rect.left - neigbourhood;
		mutable_rect.right = container_rect.right + neigbourhood;
		mutable_rect.top = container_rect.top - neigbourhood;
		mutable_rect.bottom = container_rect.bottom + neigbourhood;
		
		return !(checkBoundary(player_rect, mutable_rect))
	}	

	/*****
	*
	*	Nearest building
	*
	*****/
	var buildings = [$('#Meera'), $('#BalikaVidhya'), $('#Budh'), $('#Ram'), $('#ClockTower'), $('#malA'), $('#g3320'), $('#Vyas'), $('#Shankar'), $('#Gandhi'), $('#Krishna'), $('#temple'), $('#Bhagirath'), $('#vishwa_karma'), $('#XMLID_1785_'), $('#gymG'), $('#ANC'), $('#FD3'), $('#FD2'), $('#Rotunda'), $('#NAB'), $('#XMLID_2622_')];

	function nearest_distance(player, container){
		var player_rect = player.getBoundingClientRect();
		var container_rect = container.getBoundingClientRect();

		var vertical_middle = (player_rect.top + player_rect.bottom)/2;
		var horizontal_middle = (player_rect.left + player_rect.right)/2;

		var top = Math.abs(container_rect.top - vertical_middle),
		left = Math.abs(container_rect.left - horizontal_middle),
		right = Math.abs(horizontal_middle - container_rect.right),
		bottom =  Math.abs(vertical_middle -  container_rect.bottom);

		return Math.sqrt(Math.pow(Math.min(left, right), 2) +  Math.pow(Math.min(top, bottom),2));
	}

	var gamePlay = setInterval(function(){
		player_props.rel_y = relative_y;
		player_props.rel_x = relative_x;
		player_props.rect = player[0].getBoundingClientRect();
		// console.log(player_props.top, player_props.left)

		var final_player_props = {};

		for(i in player_props){
			final_player_props[i] = player_props[i];
		}

		move(final_player_props);
		player_props.top = 0;
		player_props.left = 0;

		var distances = [];
		buildings.forEach(function(ele, ind){
			// console.log(nearest_distance(player[0], ele[0]).toString());
			// console.log(ele)
			distances.push([ele.attr('id'), nearest_distance(player[0], ele[0]).toString()]);
		});
		// console.log(distances)
		var sorted = distances.sort(function(a, b){
			return parseInt(a[1]) - parseInt(b[1]);
		})
		var current = sorted[0][0];
		if(current=="XMLID_1785_"){
			current = "Library";
		}else if(current=="g3320"){
			current = "BirlaMemorial"; 
		}else if(current =="XMLID_2622_"){
			current = "Workshop";
		}
		window.selected = current;

		$('#dev_info span').text(current);
	

	}, 100);

	svg.append(' <use id="use1" xlink:href="#player_girl" /> <use id="use2" xlink:href="#statue1" />')


});