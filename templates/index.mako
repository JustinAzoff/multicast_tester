<table border=1>
<thead>
<tr> <th> Time </th> <th> IP </th> <th> kbytes </th> <th> mbits </th> </tr>
</thead>
<tbody>
%for x in stats:
<tr>
    <td>${x.time.strftime("%Y-%m-%d %H:%M:%S")}</td>
    <td>${x.ip}</td>
    <td>${x.kbytes}</td>
    <td>${x.mbits}</td>
</tr>
%endfor
</tbody>
</table>
