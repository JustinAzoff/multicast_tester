<%inherit file="base.mako"/>
<table class="data" border=1>
<thead>
<tr> <th> Time </th> <th> Kbytes </th> <th>mbits</th> </tr>
</thead>
<tbody>
%for x in stats:
<tr>
    <td>${x.time}</td>
    <td>${x.kbytes}</td>
    <td>${x.mbits}</td>
</tr>
%endfor
</tbody>
</table>
