<?php
if (isset($_GET['word'])) {
	$word = $_GET['word'];
	$safeword = escapeshellarg($word);
	$result  = exec("python ./assets/py/proxy.py $safeword");
	echo $result;		
} else {
	echo "SERVER_ERROR";
}

?>
