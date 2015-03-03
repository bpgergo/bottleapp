<table>
<tr>
<th>rank</th>
<th>pair</th>
<th>score</th>
<th> percentage </th>
<th> tie </th>
<th>original name1</th>
<th>original name2</th>
<th>original name3</th>
<th>resolved name1</th>
<th>resolved name2</th>
<th>resolved name3</th>
</tr>
% if ranks:
    % for rank in ranks:
        <tr>
        <td>{{ rank.rank }}</td>
        <td>{{ rank.pair }}</td>
        <td>{{ rank.score }}</td>
        <td>{{ rank.percentage }}</td>
        <td>{{ rank.tie }}</td>
        <td>{{ rank.original_name1 }}</td>
        <td>{{ rank.original_name2 }}</td>
        <td>{{ rank.original_name3 }}</td>
        <td>{{ rank.name1 }}</td>
        <td>{{ rank.name2 }}</td>
        <td>{{ rank.name3 }}</td>
        </tr>
    % end
% end
</table>
%rebase layout