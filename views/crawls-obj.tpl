<table>
<tr>
<th>Url</th>
<th>save timestamp</th>
<th>pages</th>
</tr>
% for crawl in crawls:
    <tr>
    <td> <a href="{{ crawl.url }}">{{ crawl.url }}</a></td>
    <td>{{ crawl.ts }}</td>
    <td> <a href="/pages?url={{crawl.url}}">Pages</a> </td>
    </tr>
% end
</table>
%rebase layout