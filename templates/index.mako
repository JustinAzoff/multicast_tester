<%inherit file="base.mako"/>
<table class="data" border=1>
<thead>
<tr> <th> IP </th> <th> Time </th> <th> kbytes </th> <th> mbits </th> <th> pps </th> <th> dups </th> <th> Delay </th></tr> 
</thead>
<tbody>
%for x in stats:
<tr>
    <td><a href="/ip/${x.ip}">${x.ip}</a></td>
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
