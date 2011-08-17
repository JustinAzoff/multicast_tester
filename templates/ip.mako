<%inherit file="base.mako"/>
<table class="data" border=1>
<thead>
<tr> <th> Time </th> <th> Kbytes </th> <th>mbits</th> <th> pps </th> <th> %loss</th> <th>Dups</th> <th>Delay</th></tr>
</thead>
<tbody>
%for t in tests:
<tr>
    <td><a href="/test/${t.id}">${t.time}</a></td>
    <td>${t.kbytes}</td>
    <td>${'%.2f' % t.mbits}</td>
    <td>${t.pps and ('%d' % t.pps)}</td>
    <td>${t.loss and ('%.2f' % t.loss)}</td>
    <td>${t.dups}</td>
    <td>${t.delay and ('%.3f' % t.delay)}</td>
</tr>
%endfor
</tbody>
</table>
