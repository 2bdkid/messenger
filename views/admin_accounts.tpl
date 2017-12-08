<!DOCTYPE html>

<html lang="en">
    <meta charset="UTF-8">
    <title>Accounts</title>
    <style>
    table, th, td {
        border: 1px solid black;
        border-collapse: collapse;
    }
    th, td {
        padding: 10px;
    }
    </style>
    <body>
        <h1>Accounts</h1>
        <table>
            <tr>
                <th>UID</th>
                <th>Username</th>
                <th>Password</th>
            </tr>
            % for account in accounts:
            <tr>
                <td>{{account[0]}}</td>
                <td>{{account[1]}}</td>
                <td>{{account[2]}}</td>
            </tr>
            % end
        </table>
    </body>
</html>
