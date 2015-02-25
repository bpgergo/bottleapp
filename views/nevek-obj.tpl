<table>
<tr>
<th>id</th>
<th>name</th>
<th>lev</th>
<th>point</th>
<th>play</th>
<th>kmp</th>
</tr>
% for nev in nevek:
    <tr>
    <td>{{ nev.id }}</td>
    <td>{{ nev.name }}</td>
    <td>{{ nev.lev }}</td>
    <td>{{ nev.point }}</td>
    <td>{{ nev.play }}</td>
    <td>{{ nev.kmp }}</td>
    </tr>
% end
</table>
%rebase layout