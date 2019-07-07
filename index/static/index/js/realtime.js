function showMessage(message, msgType){
	$('.messagelist .dacMsg').text(message)
	$('.messagelist .dacMsg').show(100)
	if(msgType=='error'){
		$('.messagelist .dacMsg').addClass('error')
		$('.messagelist .dacMsg').removeClass('success')
	}else{
		$('.messagelist .dacMsg').addClass('success')
		$('.messagelist .dacMsg').removeClass('error')
	}
	setTimeout(5000, function(){
		$('.messagelist .dacMsg').hide(100)
	})
}

$(document).ready(function(){
	// Toggle the search form at the nav bar
	$('.navbar-right .search').on('click', function(){
		$('.main_box .searchForm').toggleClass('hide')
	})


	var customTags = [ '<%', '%>' ];

	$('.media-body').delegate('.fellowship','click', function(){
		action = $(this).data('action')
		username = $(this).data('username')
		var self = $('.media-body .fellowship.'+username)
		$.ajax({
			url: '/api/fellowship/'+action+'/'+username,
			method: 'GET',
			success: function(data){
				if(!data){
					showMessage('Error connecting to the server', 'error')
					return;
				}else{
					if(action=='follow'){
						self.data('action', 'unfollow')
						self.text('Unfollow')
						var newFollowingTemplate = $('#followingTemplate').html()
						var dt = new Date()
						
						Templatedata = {
							username: username,
							profilePics: data,
							date: dt.toDateString()+', '+dt.toLocaleTimeString()
						}
						$('#follower .following .comment_list').after(Mustache.render(newFollowingTemplate, Templatedata))
					}else{
						self.data('action', 'follow')
						self.text('Follow')
						$('#follower .following .media-body .fellowship.'+username).closest('.review_item').remove()
					}
				}
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})

	})

	// Favour or unfavour a post on my profile
	$('.media-body').delegate('.favouring','click', function(){
		action = $(this).data('action')
		var self = $(this)
		$.ajax({
			url: '/api/favouring/'+action+'/'+$(this).data('postid'),
			method: 'GET',
			success: function(data){
				if(!data){
					showMessage('Error connecting to the server', 'error')
				}

				if(action=='unfavour'){
					self.closest('.review_box').toggle(100, function(){
						$('.favCount').text( parseInt($('.favCount').text())-1 )
					})
					self.closest('.makeblack').css('color', 'black')
					self.closest('i').data('action', 'favour')
				}else{
					self.closest('.makeblack').css('color', 'blue')
					self.closest('i').data('action', 'unfavour')
				}
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})

	})
	// Favour or unfavour a post on someone's profile
	$('.media-body').delegate('.Sinfavouring','click', function(){
		action = $(this).data('action')
		alert(action)
		var self = $(this)
		$.ajax({
			url: '/api/favouring/'+action+'/'+$(this).data('postid'),
			method: 'GET',
			success: function(data){
				if(!data){
					showMessage('Error connecting to the server', 'error')
					return;
				}else{
					if(action=='favour'){
						self.data('action', 'unfavour')
						self.text('Remove')
					}else{
						self.data('action', 'favour')
						self.text('Favour')
					}
					// if(action=='unfavour'){
					// 	self.closest('.review_box').toggle(100, function(){
					// 		$('.favCount').text( parseInt($('.favCount').text())-1 )
					// 	})
					// }
				}
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})

	})

	// Create new wall post
	$('#myTabContent').delegate('#contactForm7', 'submit', function(){
		$.ajax({
			url: '/api/mywall/',
			method: 'POST',
			data: {
				'body': $('#message5').val(),
				'user': $('#user').val(),
				'writer': parseInt($('#wall_writer').val()),
				'csrfmiddlewaretoken': $('#myTabContent #mywalltoken').text()
			},
			success: function(data){
				if(!data){
					showMessage('Error connecting to the server', 'error')
					return;
				}

				console.log(data)
				var newWallTemplate = $('#newWallPostTemplate').html();

				// Formatting the server returned date
				var dt = new Date(data.date)
				data.date = dt.toDateString()+', '+dt.toLocaleTimeString()

				// Increasing the total number of wall count
				$('#wallcount').text( parseInt($('#wallcount').text())+1 )
				$('#message5').val('')
				$('#wall .newWallTemplateClass').after(Mustache.render(newWallTemplate, data, customTags))
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})
	})

	// Handles the wall reply
	$('#myTabContent').delegate('.wallreply', 'submit', function(){
		var wallid = $(this).data('identify')
		var id = wallid.replace('replywallform', '')
		$.ajax({
			url: '/api/replywall/',
			method: 'POST',
			data: {
				'body': $('#myTabContent .wallreply #'+id+'wallreplybody').val(),
				'wall': id,
				'writer': $('#myTabContent .wallreply #'+id+'reply_writer').val(),
				'csrfmiddlewaretoken': $('#myTabContent #mywalltoken').text()
			},

			success: function(data){
				if(!data){
					showMessage('Error connecting to the server', 'error')
					return;
				}

				var newWallTemplate = $('#newWallPostTemplate').html();
				var dt = new Date(data.date)
				data.date = dt.toDateString()+', '+dt.toLocaleTimeString()
				
				// new number of commnent
				num = parseInt($('#'+id+'reply .commentCount').text()) + 1
				$('#'+id+'reply .commentCount').text(num)

				// Empty the text box
				$('#myTabContent .wallreply #'+id+'wallreplybody').val('')

				var newWallReplyTemplate = $('#wallReplyTemplate').html();
				$('#'+id+'reply .nocomment').remove(); // Remove the 'No comment yet'

				$('#myTabContent #'+id+'reply .wallreplycontainer').append(Mustache.render(newWallReplyTemplate, data))
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})
	})

	// Editing post
	$('#review').delegate('.editpostform', 'submit', function(){
		var postid = $(this).data('postid')

		$.ajax({
			url: '/api/editpost/'+$(this).data('postid')+'/',
			method: 'POST',
			data: {
				'title': $('#review .comment_list #'+postid+'edit #'+postid+'postTitle').val(),
				'body': $('#review .comment_list #'+postid+'edit #'+postid+'postBody').val(),
				'postType': $('#review .comment_list #'+postid+'edit #'+postid+'postType').val(),
				'category':$('#review .comment_list #'+postid+'edit #'+postid+'postCategory').val(),
				'csrfmiddlewaretoken': $('#review .editposttoken')[0].innerHTML
			},
			success: function(data){
				if(!data){
					showMessage('Error connecting to the server', 'error')
					return;
				}
				// Editing the content
				typeCat = data.postType+' ('+data.category+')'
				$('#review .comment_list #'+postid+'title').text(data.title)
				$('#review .comment_list #'+postid+'text').text(data.body)
				$('#review .comment_list #'+postid+'type').text(typeCat)

				$('#'+postid+'edit').css('display', 'none');
				$('#'+postid+'text').css('display', 'block');

				$('#review .media-body #'+postid+'executor').text('Edit Post')
				
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})
	})

	$('#review').delegate('#contactForm6', 'submit', function(){
		$.ajax({
			url: '/api/addpost/',
			method: 'POST',
			data: {
				'title': $('#review #title4').val(),
				'body': $('#review #body4').val(),
				'postType': $('#review #type6').val(),
				'category': $('#review #cat3').val(),
				'user': $('#review #userid').val(),
				'csrfmiddlewaretoken': $('#review #addposttoken').text()
			},
			success: function(data){
				if(!data){
					showMessage('Error connecting to the server', 'error')
					return;
				}
				console.log(data)
				var postTemplate = $('#newPostTemplate').html();
				var dt = new Date(data.date)
				data.date = dt.toDateString()+', '+dt.toLocaleTimeString()

				$('#review .newPostTemplateclass').after(Mustache.render(postTemplate, data))
				$('.col-lg-6 .postCount').text( parseInt($('.col-lg-6 .postCount').text())+1 )

				$('#review #title4').val('')
				$('#review #body4').val('')
				$('#review #type6').val('')
				$('#review #cat3').val('')
				$('#review .nopost').remove()
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})
	})

	// Handle commenting on your own post in Post(review) tab
	$('#review').delegate('.postcomment', 'submit', function(){
		var postid = $(this).data('postid')
		// var $self = $(this).closest('.postcommentClass')
		$.ajax({
			url: '/api/commentpost/',
			method: 'POST',
			data: {
				'targetpost': $('#review #'+postid+'targetpost').val(),
				'body': $('#review #'+postid+'commentbody').val(),
				'author': $('#review #'+postid+'author').val(),
				'csrfmiddlewaretoken': $('#postcommenttoken').text()
			},
			success: function(data){
				if(!data){
					showMessage('Error connecting to the server', 'error')
					return;
				}
				console.log(data)

				var postcomTemplate = $('#postCommentTemplate').html();
				var dt = new Date(data.comDate)
				data.comDate = dt.toDateString()+', '+dt.toLocaleTimeString()

				$('#review #'+postid+'reply .postcommentClass').append(Mustache.render(postcomTemplate, data))
				// $self.append(Mustache.render(postcomTemplate, data))

				$('#review .reply#'+postid+'reply .postCommentCount').text( parseInt($('#review #'+postid+'reply .postCommentCount').text())+1 )

				$('#review #'+postid+'commentbody').val('')

			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})
	})

	// Handle commenting of post in favourite(contact) tab
	$('#contact').delegate('.favourComment', 'submit', function(){
		var postid = $(this).data('postid')
		// var $self = $(this).closest('.postcommentClass')
		$.ajax({
			url: '/api/commentpost/',
			method: 'POST',
			data: {
				'targetpost': $('#contact #'+postid+'favtargetpost').val(),
				'body': $('#contact #'+postid+'favcommentbody').val(),
				'author': $('#contact #'+postid+'favauthor').val(),
				'csrfmiddlewaretoken': $('#favourcommenttoken').text()
			},
			success: function(data){
				if(!data){
					showMessage('Error connecting to the server', 'error')
					return;
				}
				console.log(data)

				var postcomTemplate = $('#postCommentTemplate').html();
				var dt = new Date(data.comDate)
				data.comDate = dt.toDateString()+', '+dt.toLocaleTimeString()

				$('#contact #2'+postid+'reply .favouredpostClass').after(Mustache.render(postcomTemplate, data))
				// $self.append(Mustache.render(postcomTemplate, data))

				$('#contact .reply#2'+postid+'reply .favpostCount').text( parseInt($('#contact .reply#2'+postid+'reply .favpostCount').text())+1 )

				$('#contact #'+postid+'favcommentbody').val('')
				// $('#contact .reply#2'+postid+' .favNocomment').remove()
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})
	})

	// Handle liking of someone's page
	$('.s_product_inner').delegate('.card_area', 'click', function(){
		username = $('.s_product_inner .card_area .lnr-diamond').data('username')
		$.ajax({
			url: '/api/likepage/'+username,
			success: function(data){
				var info = "You liked "+username+"'s page"
				if(data==info){
					showMessage(data, 'success')
					$('.s_product_inner .card_area span').text( parseInt($('.s_product_inner .card_area span').text())+1 )
					return;
				}
				showMessage(data, 'error')
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})
	})

	// Handles postcomment on a single post display
	$('.newsletter_widget').delegate('.postcomment', 'submit', function(){
		var postid = $(this).data('postid')
		// var $self = $(this).closest('.postcommentClass')
		$.ajax({
			url: '/api/commentpost/',
			method: 'POST',
			data: {
				'targetpost': $('.postcomment #'+postid+'targetpost').val(),
				'body': $('.postcomment #'+postid+'commentbody').val(),
				'author': $('.postcomment #'+postid+'author').val(),
				'csrfmiddlewaretoken': $('#postcommenttoken').text()
			},
			success: function(data){
				if(!data){
					showMessage('Error connecting to the server', 'error')
					return;
				}
				console.log(data)

				var postcomTemplate = $('#postCommentTemplate').html();
				var dt = new Date(data.comDate)
				data.comDate = dt.toDateString()+', '+dt.toLocaleTimeString()

				$('.postcommentClass').after(Mustache.render(postcomTemplate, data))

				$('.comments-area .postCommentCount').text( parseInt($('.comments-area .postCommentCount').text())+1 )

				$('.postcomment #'+postid+'commentbody').val('')
				$('.singleNoComment').remove()

			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})
	})


	// Handles username search at the nav bar
	$('.searchForm').on('submit', function(){
		var image = "<div class='center'><img src='/static/index/img/loading.gif' class='loadingImg'></div>"
		$('.searchResult').html(image)
		$.ajax({
			url: '/api/searchUsername/',
			method: 'POST',
			data: {
				'username': $('.searchForm #searchText').val(),
				'csrfmiddlewaretoken': $('.main_menu #searchToken').text()
			},

			success: function(data){
				$('.searchResult').removeClass('hide')
				$('.searchResult').html('')
				if(!data){
					$('.searchResult').html("<div class='center'>No result found</div>")
				}else{
					var newSearchResultTemplate = $('#searchResultTemplate').html();
					for(var i=0;i<data.length;i++){
						$('.searchResult').append(Mustache.render(newSearchResultTemplate, data[i]))
					}
				}
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})
	})


	// Handle post search by title
	$('.blog_area .postSearch').on('submit', function(){
		var image = "<div class='center'><img src='/static/index/img/loading.gif' class='loadingImg'></div>"
		$('.postSearchResult').html(image)
		$.ajax({
			url: '/api/searchPost/',
			method: 'POST',
			data: {
				'title': $('.blog_area .postSearch .form-control').val(),
				'csrfmiddlewaretoken': $('.blog_area .postSearch p').text()
			},

			success: function(data){
				$('.postSearchResult').removeClass('hide')
				$('.postSearchResult').html('')
				if(!data){
					$('.postSearchResult').html("<div class='center'>No result found</div>")
				}else{
					var newSearchResultTemplate = $('#postSearchResultTemplate').html();
					for(var i=0;i<data.length;i++){
						$('.postSearchResult').append(Mustache.render(newSearchResultTemplate, data[i]))
					}
				}
			},
			error: function(err){
				showMessage('Error connecting to the server', 'error')
				console.log(err)
			}
		})
	})

	$('.blog_area .postSearch').on('click', function(){
		$('.postSearchResult').toggleClass('hide')
	})

	$('.main_menu .searchForm').on('click', function(){
		$('.searchResult').toggleClass('hide')
	})
})
