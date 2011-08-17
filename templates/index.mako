<%inherit file="base.mako"/>
<p>
Stats for ${machines} machines.
<table class="data" border=1>
<thead>
<tr> <th> IP </th> <th> Time </th> <th> kbytes </th> <th> mbits </th> <th> pps </th> <th> %loss </th> <th> Delay </th> <th>Adjusted rate</th></tr> 
</thead>
<tbody>
%for x in stats:
<tr>
    <td><a href="/ip/${x.ip}">${x.ip}</a></td>
    <td>${x.time}</td>
    <td>${x.kbytes}</td>
    <td>${'%.2f' % x.mbits}</td>
    <td>${x.pps and ('%d' % x.pps)}</td>
    <td>${x.loss and ('%.2f' % x.loss)}</td>
    <td>${x.delay and ('%.3f' % x.delay)}</td>
    <td>${(x.mbits > 90 and x.delay) and int(x.mbits*60/(60+x.delay)) or ''}</td>
</tr>
%endfor
</tbody>
</table>
