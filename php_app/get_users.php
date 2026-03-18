<?php
include 'db.php';

$sql = "SELECT id, name, email FROM users";
$result = $conn->query($sql);

$data = [];

while($row = $result->fetch_assoc()) {
    $data[] = $row;
}

echo json_encode($data);
?>
