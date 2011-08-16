<%inherit file="base.mako"/>
<table class="data" border=1>
<thead>
<tr> <th> IP </th> <th> Last </th> <th>Samples</th> <th> min </th> <th> max </th> <th> avg </th> <th> pps </th> <th> dups </th> </tr> 
</thead>
<tbody>
%for x in stats:
<tr>
    <td><a href="/ip/${x.ip}">${x.ip}</a></td>
    <td>${x.last}</td>
    <td>${x.samples}</td>
    <td>${x.min}</td>
    <td>${x.max}</td>
    <td>${x.avg}</td>
    <td>${x.pps}</td>
    <td>${x.dups}</td>
</tr>
%endfor
</tbody>
</table>
