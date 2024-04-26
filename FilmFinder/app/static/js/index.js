function login() {
    var user_name = $('#loginUsername').val();
    var password = $('#loginPassword').val();
    
    $.ajax({
        type: 'POST',
        url: '/login',
        contentType: 'application/json',
        data: JSON.stringify({ user_name: user_name, password: password }),
        success: function(response) {
            if (response.success) {
                alert('Login successful!');
                // Redirect to search page on successful login
                window.location.href = '/search-page';
            } else {
                alert('Login failed: ' + response.message);
            }
        },
        error: function() {
            alert('An error occurred while processing your request.');
        }
    });
}

function register() {
    var user_name = $('#registerUsername').val();
    var password = $('#registerPassword').val();
    
    $.ajax({
        type: 'POST',
        url: '/register',
        contentType: 'application/json',
        data: JSON.stringify({ user_name: user_name, password: password }),
        success: function(response) {
            if (response.success) {
                alert('Registration successful!');
                // Redirect or perform any other actions on successful registration
            } else {
                alert('Registration failed: ' + response.message);
            }
        },
        error: function() {
            alert('An error occurred while processing your request.');
        }
    });
}
