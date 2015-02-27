<table>
<tr>
<th>Url</th>
<th>save timestamp</th>
<th>ranks</th>
</tr>
% for page in pages:
    <tr>
    <td> <a href="{{ page.url }}">{{ page.url }}</a></td>
    <td>{{ page.ts }}</td>
    <td> <a href="/ranks?url={{page.url}}">Ranks</a> </td>
    </tr>
% end
</table>
%rebase layout