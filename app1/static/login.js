function login() {
  email = document.getElementById('email')
  password = document.getElementById('password')
  fetch('/login', {
    method: 'POST',
    body: JSON.stringify({ email: email.value, password: password.value }),
    headers:  { 'Content-Type': 'application/json' }
  })
  .then(function success(res) {
    if(res.status != 200) { throw new Error('Login Failed') }
    return res.json()
  }).then(function jsonHandler(res) {
    document.cookie = `token=${res['token']};expiry=${res['expiry']}`
    window.location.href = '/'
  })
    .catch(function catchErr(err) {
    console.error(err)
    throw new Error('something exploded.')
  })
  password.value = ''
  email.value = ''
}

function register() {
  email = document.getElementById('email')
  password = document.getElementById('password')
  fetch('/register', {
    method: 'POST',
    body: JSON.stringify({ email: email.value, password: password.value }),
    headers:  { 'Content-Type': 'application/json' }
  })
  .then(function success(res) {
    window.location.href = '/login_page'
  }).catch(function catchErr(err) {
    console.error(err)
    throw new Error('something exploded.')
  })
  password.value = ''
  email.value = ''
}

