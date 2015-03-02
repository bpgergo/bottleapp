<table>
<tr>
<th>alias</th>
<th>name</th>
<th>generator</th>
<th>approved</th>
</tr>
% for alias in aliases:
    <tr>
    <td>{{ alias.alias }}</td>
    <td>{{ alias.name }}</td>
    <td>{{ alias.generator }}</td>
    <td>{{ alias.approved }}</td>
    </tr>
% end
</table>
%rebase layout