<?php
	
    // include db connect class
    //require_once __DIR__ . '/db_connect.php';

    // connecting to db
    //$db = new DB_CONNECT();

    $servername = "localhost";
    $username =  "root";
    $password = "password";
    $dbName = "light_control";    
	
    //Make Connection
    $conn = new mysqli($servername, $username, $password, $dbName);
    //Check Connection
    if(!$conn){
	echo " can't connect ";
	die("Connection Failed. ". mysqli_connect_error());
    }

	
    $sql = "SELECT ID, light_1, light_2, light_3 FROM brightness";
    $result = mysqli_query($conn,$sql);
	
	
    if(mysqli_num_rows($result) > 0){
	
    //show data for each row
    //while($row = mysqli_fetch_assoc($result)){
    $row = mysqli_fetch_assoc($result);
    //echo "ID:".$row['ID'] . "|light_1:".$row['light_1']."|light_2:".$row['light_2']. "|light_3:".$row['light_3'];
    echo $row['light_1']; 
    //}
  }

?>
