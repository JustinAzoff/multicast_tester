<table border=1>
<thead>
<tr> <th> IP </th> <th> Last </th> <th>Samples</th> <th> min </th> <th> max </th> <th> avg </th> </tr>
</thead>
<tbody>
%for x in stats:
<tr>
    <td>${x.ip}</td>
    <td>${x.last}</td>
    <td>${x.samples}</td>
    <td>${x.min}</td>
    <td>${x.max}</td>
    <td>${x.avg}</td>
</tr>
%endfor
</tbody>
</table>
