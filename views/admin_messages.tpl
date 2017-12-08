<!DOCTYPE html>

<html lang="en">
    <head>
        <meta charset="UTF-8">
        <title>Messages</title>
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
        <h1>Messages</h1>
        <table>
            <tr>
                <th>FROM</th>
                <th>TO</th>
                <th>MESSAGE</th>
            </tr>
            % for message in messages:
            <tr>
                <td>{{message[0]}}</td>
                <td>{{message[1]}}</td>
                <td>{{message[2]}}</td>
            </tr>
            % end
        </table>
    </body>
</html>
