<?php

require_once '../open_db.php';

$sql =
  'CREATE TABLE subjects_mar( '.
  'suj_no SERIAL, '.
  'usr_name TEXT NOT NULL, '.
  'mdp VARCHAR(8) NOT NULL, '.
  'ip_add TEXT, '.
  'wid TEXT, '.
  'genre VARCHAR(1), '.
  'age INT, '.
  'french TEXT, '.
  'ens_test1 TEXT, '.
  'ens_test2 TEXT, '.
  'cond TEXT, '.
  'prov TEXT, '.
  'errors INT, '.
  'rappel INT, '.
  'version INT, '.
  'comp INT, '.
  'primary key ( suj_no ))';


$stmt = $conn->prepare($sql); // On obtient l'instance de la classe PDOStatement qui correspond à cette requête
$stmt->execute();

$sql =
  'CREATE TABLE time_mar( '.
  'suj_no INT, '.
  'time TEXT, '.
  'nature TEXT)';

$stmt = $conn->prepare($sql); // On obtient l'instance de la classe PDOStatement qui correspond à cette requête
$stmt->execute();


$sql =
  'CREATE TABLE test1_mar( '.
  'suj_no INT, '.
  'essai INT, '.
  'stem TEXT, '.
  'target TEXT, '.
  'ans TEXT, '.
  'corr INT)';

$stmt = $conn->prepare($sql); // On obtient l'instance de la classe PDOStatement qui correspond à cette requête
$stmt->execute();

$sql =
  'CREATE TABLE test2_mar( '.
  'suj_no INT, '.
  'essai INT, '.
  'stem TEXT, '.
  'target TEXT, '.
  'ans TEXT, '.
  'corr INT)';

$stmt = $conn->prepare($sql); // On obtient l'instance de la classe PDOStatement qui correspond à cette requête
$stmt->execute();

$sql =
  'CREATE TABLE quest_mar( '.
  'suj_no INT, '.
  'perc_corr1 TEXT, '.
  'perc_corr2 TEXT, '.
  'impr TEXT, '.
  'notes TEXT, '.
  'strategy TEXT, '.
  'concentrated1 INT, '.
  'concentrated2 INT, '.
  'interest TEXT, '.
  'tired1 INT, '.
  'tired2 INT, '.
  'prior_hours TEXT, '.
  'restful INT, '.
  'bwtired INT, '.
  'nap_yn TEXT, '.
  'nap_min TEXT, '.
  'rested TEXT, '.
  'mornev TEXT)';

$stmt = $conn->prepare($sql); // On obtient l'instance de la classe PDOStatement qui correspond à cette requête
$stmt->execute();

$sql = 'GRANT SELECT, UPDATE, INSERT ON subjects_mar TO sujets_alfharm';

$stmt = $conn->prepare($sql); // On obtient l'instance de la classe PDOStatement qui correspond à cette requête
$stmt->execute();

$sql = 'GRANT SELECT, UPDATE, INSERT ON time_mar TO sujets_alfharm';

$stmt = $conn->prepare($sql); // On obtient l'instance de la classe PDOStatement qui correspond à cette requête
$stmt->execute();

$sql = 'GRANT SELECT, UPDATE, INSERT ON test1_mar TO sujets_alfharm';

$stmt = $conn->prepare($sql); // On obtient l'instance de la classe PDOStatement qui correspond à cette requête
$stmt->execute();

$sql = 'GRANT SELECT, UPDATE, INSERT ON test2_mar TO sujets_alfharm';

$stmt = $conn->prepare($sql); // On obtient l'instance de la classe PDOStatement qui correspond à cette requête
$stmt->execute();

$sql = 'GRANT SELECT, UPDATE, INSERT ON quest_mar TO sujets_alfharm';

$stmt = $conn->prepare($sql); // On obtient l'instance de la classe PDOStatement qui correspond à cette requête
$stmt->execute();





$conn = null;

?>

