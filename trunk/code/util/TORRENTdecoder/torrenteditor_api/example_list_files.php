<?php
/*
TorrentEditor.com API - Simple API to modify torrents
Copyright (C) 2009  Tyler Alvord

Web: http://torrenteditor.com
IRC: #torrenteditor.com on efnet.org  

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.
*/

// Set to the path that contains the TorrentEditor.com include files
set_include_path('include');
include_once('torrent.php');

// Filename of torrent to load
$torrent_file = 'example.torrent';

// Load the .torrent file contents. This could be done via file upload.
// Example loads a local file specified in $torrent_file
$data = file_get_contents($torrent_file);
if ($data == false) {
    exit("Failed to read from $torrent_file.");
}

// Create a torrent object
$torrent = new Torrent();

// Load torrent file data obtained above 
if ($torrent->load($data) == false) {
    exit("An error occured: {$torrent->error}");
}

// Add the new tracker to the torrent
$files = $torrent->getFiles();

// Loop through the trackers and display them
$count = 0;
foreach ($files as $file) {
    $count++;
    echo("$count: {$file->name} - {$file->length} bytes\n");
}

?>