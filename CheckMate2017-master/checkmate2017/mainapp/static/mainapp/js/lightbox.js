var no_of_questions=0;//length of question array per building
var questions={};//question list
var pks={};
var qVal = 1;
var stories={"Meera":"Stories for Meera","Budh":"Stories for Budh","malA":"Story for MalA"};
var xopen = false;
$(document).ready(function(){
	


	window.lightbox = lightbox;

	$('#backdrop .close').click(function(){
		$('#backdrop').fadeOut();
		xopen = false;
	})

})

function lightbox(){
	$('#backdrop').fadeIn();
	$('#backdrop .heading').text(window.selected);
	var text_content=document.getElementById('content_text');
	var buttons_and_inputs=document.getElementById('extra_part');
	var building=window.selected;
	text_content.innerHTML=stories[building];
	buttons_and_inputs.innerHTML="<button id='continue' onclick='loadQues()'>Continue...</button>";
}

function loadQues() {
	var token = document.cookie.split("=")[1];
	var buttons_and_inputs=document.getElementById('extra_part');
	var text_content=document.getElementById('content_text');
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
			while(index1 != -1){
				no_of_questions++;
				buff= msg1.substring(index1+1,index2);
				index1=msg1.indexOf("[",index2+1);
				index2=msg1.indexOf("]",index1);
				console.log(JSON.stringify(msg));
				var con=JSON.parse(buff);
				pks["pk" + no_of_questions]=con.pk;
				questions["question" + no_of_questions]=con.fields.question_text;
			}
			text_content.innerHTML=questions["question1"];
		},
		error: function(xhr){
			console.log(xhr);
		},
		type: 'POST'
	}
	$.ajax(a);
	var answer_form="<input id= 'ans' name='answer' type='text' placeholder='Answer'><button id='submit' onclick='mysubmit()'>Submit</button>";//answer form html
	buttons_and_inputs.innerHTML=answer_form;

}

function mysubmit() {

	//Answer submission data format
	var form_data={
		csrfmiddlewaretoken:document.cookie.split("=")[1],
		pkvalue:pks["pk"+qVal],
		answer:$("#ans").val()
	};
	console.log('...',pks, qVal, form_data)
	var request={
		url:"/question",
		type:"POST",
		data:form_data,
		method:'POST',
		success: function(msg)
		{
			console.log(msg);
			//update points
			$("#score").html("Points:"+msg["score"])
			updateStickers(msg.phoda, msg.lite)
			//show correct
			if(msg["status"]=="1")
				alert("correct")
			else
				alert("incorrect")

		},
		error: function(xhr)
		{
			//update points
			//show correct
			//hide box
			console.log(xhr);
		}

	};

	var response=$.ajax(request);
  }

 function query(){
 	var form_data={
		csrfmiddlewaretoken:document.cookie.split("=")[1],
 	};

 	var request={
 		url:"/query",
 		type:"GET",
 		data:form_data
 	};

 	a=$.ajax(request);
 	console.log(a);
 }

 function update_player(){

 	new_player="boy"
 	var form_data={
		csrfmiddlewaretoken:document.cookie.split("=")[1],
		player:new_player,
 	};

 	var request={
 		url:"/query",
 		type:"POST",
 		data:form_data
 	};

 	a=$.ajax(request);
 	console.log(a);
 }
