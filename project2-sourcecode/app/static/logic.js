function getToken() {
  //var cookies = document.cookie.split(';')
  //var token = cookies.filter(function filter(cookie) {
  //   return cookie.split('=').includes('token')
  //})[0]
  //return token.split('/=(.+)/')[0].split('=')[1]

	var tokens = document.cookie.split("token=");
	if (tokens.length == 2) {
		return tokens[1].split(";")[0];
	}
	return null;
}

function checkLoggedIn() {
  var token = getToken()
  console.log(token)
  if(!token) {
    window.location.href = '/login_page'
  }
  loadPosts(token)
}

function htmlEncode(value) {
     if (value) {
         return $('<div/>').text(value).html();
     } else {
         return '';
     }
 }

function loadPosts(token) {
  fetch('/message/get', {
    method: 'GET',
    headers: { token: token }
  }).then(function responseHandler(res) { return res.json() })
    .then(function messageHandler(res) {
    var list = document.getElementById('messageList')
    var posts = ''
    // run it once with eval for the friendly little scripts people write to help other users
    // if that fails just normally load the post
    for(x of res) {
      try {
        posts = posts+'<br /><li><h4>' + x['author'] + ':' + '</h4><br /><p>' + new String(eval(htmlEncode(x['content'])))) + '</p>'
      } catch(err) {
        posts = posts+'<br /><li><h4>' + x['author'] + ' says:' + '</h4><br /><p>' + x['content'] + '</p>'
      }
    }
    list.innerHTML = posts
  })
}

function newPost() {
  var post = document.getElementById('post')
  fetch('/message/new', {
    method: 'POST',
    headers: { token: getToken(), 'Content-Type': 'application/json' },
    body: JSON.stringify({ text: post.value })
  }).then(function responseHandler(res) {
    if(!res.status==200) {
      throw new Error('Couldn\'t write post.')
    }
    loadPosts(getToken())
  })
  post.value = ''

}


window.onload = checkLoggedIn
