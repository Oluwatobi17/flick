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

