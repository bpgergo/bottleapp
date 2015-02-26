<table>
<tr>
<th>rank</th>
<th>pair</th>
<th>score</th>
<th> % </th>
<th>name1</th>
<th>name2</th>
</tr>
% if ranks:
    % for rank in ranks:
        <tr>
        <td>{{ rank.rank }}</td>
        <td>{{ rank.pair }}</td>
        <td>{{ rank.score }}</td>
        <td>{{ rank.percentage }}</td>
        <td>{{ rank.name1 }}</td>
        <td>{{ rank.name2 }}</td>
        </tr>
    % end
% end
</table>
%rebase layout