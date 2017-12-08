<!DOCTYPE html>

<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Messenger App</title>
    </head>
    <body>
        <h1>Messenger Login</h1>
        <form action="/messenger/login" method="POST" id="login_form">
            <label for="username">Username</label>
            <input type="text" name="username" id="username" required>
            <br>
            <label for="password">Password</label>
            <input type="password" name="password" id="password" required>
            <br>
            <input type="submit" value="Login">
            <input type="submit" name="register" value="Register">
        </form>
    </body>
</html>
