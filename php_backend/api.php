<?php
header('Content-Type: application/json');
$posts = json_decode(file_get_contents(__DIR__ . '/posts.json'), true);
echo json_encode($posts);
