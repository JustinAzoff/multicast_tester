<!DOCTYPE html>
<html>
<head>
<style type="text/css">
table.data {
    border: 1px solid black; 
    border-collapse: collapse;
}
table.data th, table.data td {
    border: 1px solid black;
    padding: 5px;
}
table.data th {
    background: lightgray;
    text-transform: capitalize;
    cursor: pointer;
}
table.data thead tr .headerSortDown, table.data thead tr .headerSortUp {
background-color: #8dbdd8;
}
</style>
<title>
Multicast Stats
%if title:
- ${title}
%endif
</title>
<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.6.2/jquery.min.js"></script>
<script src="/static/jquery.tablesorter.min.js"></script>
<script>
$(document).ready(function(){ 
    $("table.data").tablesorter(); 
}); 
</script>
</head>
<body>

<h1>Multicast Stats
%if title:
- ${title}
%endif
</h1>

${self.body()}

</body>
</html>
