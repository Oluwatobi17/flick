function getCookie(name) {
    var cookieValue = null;
    if(document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for(var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if(cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
// $("#contactForm7 input[name='csrfmiddlewaretoken']")[0].value

function writeonwall(){
	console.log('Hello')
	/*var t = $('#contactForm7 input[type='hidden', name='csrfmiddlewaretoken']')
	console.log()*/
	console.log($('#contactForm7').closest('form'))
	$.ajax({
		url: '/api/wall/',
		method: 'post',
		data: {
			'user': $('#wallowner')[0].innerText,
			'body': $('#message5')[0].innerText
		},
		success: function(data){
			console.log('Hello that was successfull')
		},
		error: function(err){
			console.log('An error:')
			console.log(err)
		}
	})
}