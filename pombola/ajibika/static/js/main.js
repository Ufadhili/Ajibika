	$(function(){
		 $('.carousel').carousel({
		        interval: 5000 //changes the speed
			    });

		 //Ugly hack for youtube embeds.
console.log("ajibika")

		 var regExp = /^.*(youtu.be\/|v\/|u\/\w\/|embed\/|watch\?v=|\&v=)([^#\&\?]*).*/;
		 var url = $("#video-frame").attr("value");
		 var match = url.match(regExp);
		 if (match && match[2].length == 11) {
		 	var myId = match[2];
		 	var src = "//www.youtube.com/embed/" + myId + "";
		 	var code = 
		 	"<iframe id='featured-vid' width='100%' height='305' src='"+src+"'frameborder='0' allowfullscreen></iframe>";
			 	$("#video-frame").replaceWith(code);		 	
				 } 

		 // If we didn't find videos for this county default to this.

		 else {		 	
		 	var code = "<iframe id='featured-vid' width='100%' height='305' src='//www.youtube.com/embed/Z4IeRbDqMnE'frameborder='0' allowfullscreen></iframe>";
		 	$("#video-frame").replaceWith(code)
		 }
	// }
	})