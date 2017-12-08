<!DOCTYPE html>

<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>{{group_name}}</title>
        <style>
        table, th, td {
            border: 1px solid black;
            border-collapse: collapse;
        }
        th, td {
            padding: 10px;
        }
        </style>
    </head>
    <body>
        <h1>{{group_name}}</h1>
        <table>
            <tr>
                <th>From</th>
                <th>Message</th>
            </tr>
            % for message in messages:
            <tr>
                <td>{{message[0]}}</td>
                <td>{{message[1]}}</td>
            </tr>
            % end
        </table>
        <h2>Reply</h2>
        <form action="/messenger/groupreply/{{group_name}}" method="POST">
            <input type="text" id="message" name="message" required>
            <input type="submit" name="submit" value="Send">
        </form>
        <h2>Add to Group</h2>
        <form action="/messenger/groupadd/{{group_name}}" method="POST">
            <input type="text" name="name" required>
            <input type="submit" name="submit" value="Send">
        </form>
    </body>
</html>
