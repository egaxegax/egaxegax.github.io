<?php 

$purl = parse_url("$_SERVER[REQUEST_URI]");
if(isset($purl['query'])){
  parse_str($purl['query'], $qstr);
  header('Content-Type: text/xml');
  echo file_get_contents($qstr['url']);
} else {
  phpinfo();
}