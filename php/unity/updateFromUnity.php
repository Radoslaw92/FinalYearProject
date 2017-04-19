<?php
//Variables for the connection
	$servername = "localhost";
	$server_username =  "root";
	$server_password = "password";
	$dbName = "light_control";
	
	 $brightness = $_POST['brightness'];
	
	//Make Connection
	$conn = new mysqli($servername, $server_username, $server_password, $dbName);
	//Check Connection
	if(!$conn){
		die("Connection Failed. ". mysqli_connect_error());
	}
	
	$sql = "UPDATE brightness SET light_1 = '$brightness' WHERE ID = '1'";
	$result = mysqli_query($conn ,$sql);
	
	if(!result) echo "error";
	else echo "Updating completed!";

?>
