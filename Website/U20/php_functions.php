<?php

function read_csv($csvfile) {
  $array = $fields = array();
  $i = 0;

  $handle = @fopen($csvfile, "r");
  if ($handle) {
    while ( ($row = fgetcsv($handle, 4096)) !== FALSE ) {
      if (empty($fields)) {
	$fields = $row; // loads header into $fields
	continue;
      }
      foreach ($row as $k => $value) {
	$array[$i][$fields[$k]] = $value;
      }
      $i++;
    }
    if (!feof($handle)) {
      echo "Error...";
    }
    fclose($handle);
  }
  return $array;
}

function generateRandomString($length = 10) {
    $characters = '0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ';
    $charactersLength = strlen($characters);
    $randomString = '';
    for ($i = 0; $i < $length; $i++) {
        $randomString .= $characters[rand(0, $charactersLength - 1)];
    }
    return $randomString;
}

function dateDifference($date_1 , $date_2 , $differenceFormat = '%a' )
{
    $datetime1 = date_create($date_1);
    $datetime2 = date_create($date_2);
    
    $interval = date_diff($datetime1, $datetime2);
    
    return $interval->format($differenceFormat);
    
}

function nettoyer($s)
{
  $stripped = preg_replace('/\W+/', '_', $s);

  return $stripped;
}

?>