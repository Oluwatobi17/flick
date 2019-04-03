var key = true;
function viewComment(operator) {
	$(document).ready(function(){
		if(key==false){
			$('#'+operator+'reply').css('display', 'none');
			$('#'+operator).text('View comments');
			key = true;
		}else{
			$('#'+operator+'reply').css('display', 'block');
			$('#'+operator).text('Hide comments');
			key = false;
		}
	})
}
var key1 = true;
function viewComment2(operator) {
	$(document).ready(function(){
		if(key1==false){
			$('#'+operator+'reply').css('display', 'none');
			$('#'+operator).html('↡');
			key1 = true;
		}else{
			$('#'+operator+'reply').css('display', 'block');
			$('#'+operator).text('↠');
			key1 = false;
		}
	})
}
var key2 = true;
function editPost(operator){
	$(document).ready(function(){
		if(key2==false){
			$('#'+operator+'edit').css({
				display: 'none'
			});
			$('#'+operator+'text').css('display', 'block');
			$('#'+operator+'executor').text('Edit Post')
			key2 = true;
		}else{
			$('#'+operator+'edit').css('display', 'block');
			$('#'+operator+'edit').removeClass('reply');

			$('#'+operator+'text').css('display', 'none');
			$('#'+operator+'executor').text('Cancel')
			key2 = false;
		}
	})
}
/*
$(document).ready(function(){
	console.log('Function entry');
	if($('#area').text()=='profile'){
		$('.navbar-nav #home').addClass('active')
		$('.menu_nav li').find('.active').removeClass('active');
		console.log('home');
	}else if($('#area').text()=='home'){
		$('.navbar-nav #profile').find('.active').removeClass('active');
		$('.menu_nav li').addClass('active')
		console.log('profile');
	}
	else if($('#area').text()=='pages'){
		$('.navbar-nav .pages').addClass('active')
		$('#navbarSupportedContent').find('.active').removeClass('active');
		console.log('pages');
	}else if($('#area').text()=='contact'){
		$('.navbar-nav .contact').addClass('active')
		console.log('contact');
		$('#navbarSupportedContent').find('.active').removeClass('active');
	}
})*/