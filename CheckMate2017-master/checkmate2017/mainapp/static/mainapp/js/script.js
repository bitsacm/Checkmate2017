// add id = player_girl to girl's g tag
$(document).ready(function(){

	// developer_info
	// $('body').append('<div id="dev_info"><h1>#prototype</h1><span></span></div>');
	

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
		width: player[0].getBoundingClientRect().width 
	}

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
		render(player_props.top,player_props.left);
	})
	
	// storing each state
	var history = [[-250, 20], [-250, 20]];

	// render animation
	function render(top, left){
		var inRoad = false;

		player_props.rel_x +=  left;
		player_props.rel_y +=  top;
	
		TweenMax.to(player, .5,{xPercent:(player_props.rel_x ), yPercent:(player_props.rel_y)});

		roads.each(function(ind, ele){
			if(checkEnclosed(player[0], $(ele)[0])){
				inRoad = true;
				old_road = $(ele);
			}
		})
		
		if(inRoad){
			history.push([player_props.rel_x, player_props.rel_y]);
		}else{
			[[player_props.rel_x, player_props.rel_y]] = history.slice(-3, -2);
			TweenMax.to(player, .1,{xPercent:(player_props.rel_x ), yPercent:(player_props.rel_y)});
			history.push([player_props.rel_x, player_props.rel_y]);

		}
		update_viewPort_coords(0);

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
			console.log('called', parent_rect)
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
			  ease:Circ.easeOut
			});
		}

	}

	// function animate_viewport(){
	// 	// $(svg[0].attributes.getNamedItem("viewBox")).animate({'value': viewport_coords.x+ " " +viewport_coords.y + " " + $(window).width()+ " "+ $(window).height()});
	// 	if(viewport_coords.prev_x !=viewport_coords.x ||viewport_coords.prev_y != viewport_coords.y){
	// 		var initial_x = viewport_coords.prev_x;
	// 		var initial_y = viewport_coords.prev_y;
	// 		viewport_coords.prev_x = viewport_coords.x;
	// 		viewport_coords.prev_y = viewport_coords.y

	// 		TweenMax.to(, 5, {
	// 		      var: 100, 
	// 		      onUpdate: function () {
	// 		          console.log(Math.ceil(counter.var));
	// 		      },
	// 		      ease:Circ.easeOut
	// 		  });

	// 	}

	// 	svg[0].attributes.getNamedItem("viewBox").value = (viewport_coords.x+ " " +viewport_coords.y + " " + $(window).width()+ " "+ $(window).height());
	// 	requestAnimationFrame(animate_viewport)
	// }

	// animate_viewport();
	
	// returns true if  enclosing
	function checkEnclosed(player, container){
		var player_rect = player.getBoundingClientRect();
		var container_rect = container.getBoundingClientRect();

		// boundary checking
		var cond_right = ((player_rect.right) >(container_rect.left ) && (player_rect.right ) < container_rect.right),
		cond_left = 	((player_rect.left) > container_rect.left && (player_rect.left) < container_rect.right),
		cond_top = 	((player_rect.top)> container_rect.top) && ((player_rect.top) < container_rect.bottom),
		cond_bottom = ((player_rect.bottom ) > container_rect.top) && ((player_rect.bottom )< container_rect.bottom);
	
		return (cond_right && cond_left && cond_top && cond_bottom)
	}

	/*****
	*
	*	Nearest building
	*
	*****/
	var buildings = [$('#Meera'), $('#BalikaVidhya'), $('#Budh'), $('#Ram'), $('#ClockTower'), $('#malA'), $('#g3320'), $('#Vyas'), $('#Shankar'), $('#Gandhi'), $('#Krishna'), $('#temple'), $('#Bhagirath'), $('#vishwa_karma'), $('#XMLID_1785_'), $('#gymG'), $('#ANC'), $('#FD3'), $('#FD2'), $('#Rotunda'), $('#NAB')];

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

	var display_buildings = setInterval(function(){
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
		window.selected = current;

		$('#dev_info span').text(sorted[0][0]);
		
		// if($('#building_names').text() != current){
		// 	$('#building_names').fadeOut(200);
		// 	var k = setTimeout(function(){
		// 		$('#building_names').text(current);
		// 		$('#building_names').css({'top': ($('#'+ sorted[0][0]).offset().top + $('#'+ sorted[0][0])[0].getBoundingClientRect().height/2 - $('#building_names').height()/2), 'left': ($('#'+ sorted[0][0]).offset().left + $('#'+ sorted[0][0])[0].getBoundingClientRect().width/2 - $('#building_names').width()/2)});
		// 		$('#building_names').fadeIn();
		// 	},200);

		// }
			
	}, 1000);


});