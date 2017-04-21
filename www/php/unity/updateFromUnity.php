<?php
//Variables for the connection
	$servername = "localhost";
	$server_username =  "root";
	$server_password = "password";
	$dbName = "light_control";
	
	$brightness = $_POST['brightness'];
	$light = $_POST['light'];
	$status = $_POST['status'];	

	//Make Connection
	$conn = new mysqli($servername, $server_username, $server_password, $dbName);
	//Check Connection
	if(!$conn){
		die("Connection Failed. ". mysqli_connect_error());
	}
	
	$sql = "UPDATE brightness SET $light = '$brightness' WHERE ID = '1'";
	$result = mysqli_query($conn ,$sql);
	$sql2 = "UPDATE status SET $light = '$status' WHERE ID = '1'";
        $result2 = mysqli_query($conn ,$sql2);

	if(!result) echo "error";
	else echo "Updating completed!";

?>
