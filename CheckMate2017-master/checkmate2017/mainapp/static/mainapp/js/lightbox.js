$(document).ready(function(){
	$('#backdrop').fadeOut(0);

	function lightbox(){
		$('#backdrop').fadeIn();
		$('#backdrop .heading').text(window.selected);
	var token = document.cookie.split("=")[1];
		var a = {
	url: '/game',
	data: {
		csrfmiddlewaretoken: token,
		bquery: window.selected,		
	},
	success: function(msg){
		console.log(msg);	
	},
	error: function(xhr){
		console.log(xhr);
	},
	type: 'POST'
}
	$.ajax(a);
	}
	window.lightbox = lightbox;

	$('#backdrop .close').click(function(){
		$('#backdrop').fadeOut();
	})

})