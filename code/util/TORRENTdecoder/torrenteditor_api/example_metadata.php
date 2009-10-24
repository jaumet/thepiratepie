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

// Filename of torrent to load and new filename for modified torrent
$torrent_file = 'example.torrent';
$save_as_file = 'example_metadata.torrent';

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

/*
Metadata that can be read/changed:
Creation Date
Comment
Created By
Piece Length (Read Only)
*/

// Display metadata
$date = date('m/d/y h:i:s', $torrent->getCreationDate());
echo("Creation Date: $date\n");
echo("Comment: {$torrent->getComment()}\n");
echo("Created By: {$torrent->getCreatedBy()}\n");
echo("Piece Length: {$torrent->getPieceLength()} bytes\n");

// Modify metadata
$torrent->setCreationDate(time()); // Update creation date to current date/time
$torrent->setComment('Torrent modified with TorrentEditor.com API');
$torrent->setCreatedBy('TorrentEditor.com API');

echo("\n--After Edit--\n\n");

// Display metadata again
$date = date('m/d/y h:i:s', $torrent->getCreationDate());
echo("Creation Date: $date\n");
echo("Comment: {$torrent->getComment()}\n");
echo("Created By: {$torrent->getCreatedBy()}\n");
echo("Piece Length: {$torrent->getPieceLength()} bytes\n");

// Save the modified torrent to $save_as_file
$data = $torrent->bencode();
if (file_put_contents($save_as_file, $data) == false) {
    exit("Failed to write to $save_as_file.");
}

?>