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
}
</style>
<title>
Multicast Stats
%if title:
- ${title}
%endif
</title>
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
