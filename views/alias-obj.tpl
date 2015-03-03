<table>
<tr>
<th>name</th>
<th>alias1</th>
<th>alias2</th>
<th>alias3</th>
<th>alias4</th>
<th>alias5</th>
<th>generator</th>
<th>approved</th>
</tr>
% for alias in aliases:
    <tr>
    <td>{{ alias.name }}</td>
    <td>{{ alias.alias1 }}</td>
    <td>{{ alias.alias2 }}</td>
    <td>{{ alias.alias3 }}</td>
    <td>{{ alias.alias4 }}</td>
    <td>{{ alias.alias5 }}</td>
    <td>{{ alias.generator }}</td>
    <td>{{ alias.approved }}</td>
    </tr>
% end
</table>
%rebase layout