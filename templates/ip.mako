<%inherit file="base.mako"/>
<table class="data" border=1>
<thead>
<tr> <th> idx </th> <th> Time </th> <th> Kbytes </th> <th>mbits</th> <th> pps </th> <th>Dups</th> <th>Delay</th></tr>
</thead>
<tbody>
%for x in stats:
<tr>
    <td>${x.idx}</td>
    <td>${x.time}</td>
    <td>${x.kbytes}</td>
    <td>${x.mbits}</td>
    <td>${x.pps}</td>
    <td>${x.dups}</td>
    <td>${x.delay and ('%.3f' % x.delay)}</td>
</tr>
%endfor
</tbody>
</table>
