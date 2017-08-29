$(document).ready(function(){
	$('#backdrop').fadeOut(0);

	function lightbox(){
		$('#backdrop').fadeIn();
		$('#backdrop .heading').text(window.selected);
	}
	window.lightbox = lightbox;

	$('#backdrop .close').click(function(){
		$('#backdrop').fadeOut();
	})

})