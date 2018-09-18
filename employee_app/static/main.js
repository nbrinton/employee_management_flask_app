
/*
This functtion clears the message_div in layout.html from the screen after waiting 5 seconds after loading
*/
function clear_messages() {
	var message_div = document.getElementById('message_div');
	if (message_div != null) {
		setTimeout(function(){
			message_div.style.display = "none";
		}, 5000);
	}
}
