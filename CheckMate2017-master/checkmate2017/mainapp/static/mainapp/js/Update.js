$(document).ready(function(){
    UpdateList();
});

delay=3000
function UpdateList() {
    //console.log("UpdateList is working");

    $.ajax({

        url : "/pingservers",//instead of ranks the tag for rank.
        type : "GET",
        dataType : "json",
        success: function(response){
        console.log("response from server")
	console.log(response)
		
		var leaderboard=document.getElementById('leaderboard')
		var ele= document.getElementById('results')
		leaderboard.removeChild(ele)
		//clear children of leaderboard
		var ele=$("<table></table>");
		$('#leaderboard').append(ele);
		ele.attr('id','results');
            for(var i=0;i<20;i++){
                $('#results').append("<tr id=" + (i+1) +"> " + "<td>"+ (i+1) + "</td>"+ "<td>" + response[i]['Teamname'] + "</td>" + "<td>"+response[i]['Score'] + "</td>"+"</tr>");
                console.log(response[i]);
	    }

        console.log(response);
        console.log("success");

    },
    error : function(xhr,errmsg,err) {
        console.log(xhr)
        $('#results').html("<div class='alert-box alert radius' data-alert>Oops! We have encountered an error: "+errmsg ); // addind the error to the dom
        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
    } 

    })

    setTimeout(UpdateList,delay);
}
	
function OrderListBy(prop) {
    return function (a, b) {
        if (a[prop] > b[prop]) {
            return 1;
        }
        else if (a[prop] < b[prop]) {
            return -1;
        }
        return 0;
    }
}
