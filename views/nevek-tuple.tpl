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
    <td>{{ nev[0] }}</td>
    <td>{{ nev[1] }}</td>
    <td>{{ nev[2] }}</td>
    <td>{{ nev[3] }}</td>
    <td>{{ nev[4] }}</td>
    <td>{{ nev[5] }}</td>
    </tr>
% end
</table>
%rebase layout