<!DOCTYPE html>

<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Messages from {{sender}}</title>
        <style>
            table, th, td {
                border: 1px solid black;
                border-collapse: collapse;
            }
            th, td {
                padding: 10px;
            }
            .messagebox {
                width: 300px;
                height: 300px;
            }
        </style>
    </head>
    <body>
        <h1>Messages from {{sender}}</h1>
        <table>
            <tr>
                <th>From</th>
                <th>Message</th>
                <th>Date</th>
            </tr>
            % for message in messages:
            <tr>
                <td>{{message[0]}}</td>
                <td>{{message[1]}}</td>
                <td>{{message[2]}}</td>
            </tr>
            % end
        </table>
        <h2>Reply</h2>
        <form action="/messenger/reply/{{sender}}" method="POST" id="reply">
            <textarea name="message" form="reply" class="messagebox"></textarea>
            <br>
            <input type="submit" name="submit" value="Send">
        </form>
    </body>
</html>
