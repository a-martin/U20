<?php

require_once '/home/martin/.base-data.php';

try
{
    /* Connection */
    $conn = new PDO($DSN, $USER_SUJ, $PASSWD);
    /* Générer des exceptions en cas d'anomalie */
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
}
catch (PDOException $e)
{
    echo 'Error PDO: ' . $e->getMessage();
}

?>