<?php
	
    // include db connect class
    //require_once __DIR__ . '/db_connect.php';

    // connecting to db
    //$db = new DB_CONNECT();

    $servername = "localhost";
    $username =  "root";
    $password = "password";
    $dbName = "light_control";    
	
    $light = $_POST['light'];
    
    //Make Connection
    $conn = new mysqli($servername, $username, $password, $dbName);
    //Check Connection
    if(!$conn){
	echo " can't connect ";
	die("Connection Failed. ". mysqli_connect_error());
    }

	
    $sql = "SELECT $light FROM brightness WHERE ID = 1";
    $result = mysqli_query($conn,$sql);
    $sql2 = "SELECT $light FROM status WHERE ID = 1";
    $result2 = mysqli_query($conn,$sql2);

	
	
    //if(mysqli_num_rows($result) > 0 && mysqli_num_rows($result2) > 0)){
    if(mysqli_num_rows($result) > 0){	
    //show data for each row
    //while($row = mysqli_fetch_assoc($result)){
    $rowBright = mysqli_fetch_assoc($result);
    $rowStatus = mysqli_fetch_assoc($result2);
    //echo "ID:".$row['ID'] . "|light_1:".$row['light_1']."|light_2:".$row['light_2']. "|light_3:".$row['light_3'];
    echo $rowBright[$light]."|". $rowStatus[$light]; 
    //}
  }

?>
