var no_of_questions=0;//length of question array per building
var questions={};//question list

$(document).ready(function(){
	$('#backdrop').fadeOut(0);

	function lightbox(){
		$('#backdrop').fadeIn();
		$('#backdrop .heading').text(window.selected);
	var token = document.cookie.split("=")[1];
		var content=document.getElementById('content');
		var a = {
			url: '/game',
			data: {
				csrfmiddlewaretoken: token,
				bquery: window.selected,
			},
			success: function(msg){
				no_of_questions=0;
				var msg1=JSON.stringify(msg);
				var buff;//read per question
				var index1=msg1.indexOf("[");
				var index2=msg1.indexOf("]");
				var inner="<select id='qlist'>";
				while(index1 != -1){
					no_of_questions++;
					buff= msg1.substring(index1+1,index2);
					index1=msg1.indexOf("[",index2+1);
					index2=msg1.indexOf("]",index1);
					console.log(JSON.stringify(msg));
					var con=JSON.parse(buff);
					questions["question" + no_of_questions]=con.fields.question_text;
					inner = inner + "<option style='width:60%;' value ='" + no_of_questions + "'>Question " + no_of_questions + "</button><br/>";
				}
				content.innerHTML=inner+"</select> <button onclick='loadQues()'>Load Question</button>";
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

function loadQues() {
	var answer_form="<br/><form action='#'><input type='text' placeholder='Answer'><input type='submit' label='submit'></form>";//answer form html
	var content=document.getElementById('content');
	var selectList=document.getElementById('qlist');
	var questionVal=selectList.options[selectList.selectedIndex].value;
	content.innerHTML=questions["question"+questionVal] + answer_form;
}
