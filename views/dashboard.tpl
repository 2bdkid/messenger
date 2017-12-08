<!DOCTYPE html>

<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Messenger Dashboard</title>
        <style>
            .messagebox {
                width: 300px;
                height: 300px;
            }
        </style>
    </head>
    <body>
        <h1>Dashboard</h1>
        <h2>Compose</h2>
        <form action="/messenger/send" method="POST" id="compose">
            <textarea name="message" form="compose" class="messagebox"></textarea>
            <br>
            <label for="recipient">To:</label>
            <input type="text" id="recipient" name="recipient" required>
            <input type="submit" name="submit" value="Send">
        </form>
        <h2>Read</h2>
        <ul>
            % for message in messages:
            <li><a href="/messenger/read/{{message}}">{{message}}</a></li>
            % end
        </ul>
        <h2>Groups</h2>
        <ul>
            % for group in groups:
            <li><a href="/messenger/group/{{group}}">{{group}}</a></li>
            % end
        </ul>
        <form action="/messenger/group/create" method="POST">
            <label for="groupname">Create new group:</label>
            <input type="text" id="groupname" name="groupname">
            <input type="submit" name="submit" value="Create">
        </form>
    </body>
</html>
