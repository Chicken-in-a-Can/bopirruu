<?php
/**
 * Author: Aspen B
 * Date: 5/14/22-5/15/22
 * Description:
 * Backend server code for bopirruu, both the cli and gui interfaces depend on this
 */

ini_set('display_errors', 1);
ini_set('display_startup_errors', 1);
error_reporting(E_ALL);

$bor_dir = "./bor";

if (isset($_GET['query'])) {
    $query = $_GET['query'];
    
    // make sure the directory exsits
    if (is_dir($bor_dir)) {
        // open it as a dir
        if ($dh = opendir($bor_dir)) {
            // loop through all files in the directory
            while (($file = readdir($dh)) !== false) {
                // make sure we don't search . and .. or hidden files
                if ((str_starts_with($file, ".")) !== true) {
                    // check if the package name contains the search query
                    if (strpos($file, $query) !== false) {
                        echo $file . ",";
                    }
                }
            }
            closedir($dh);
        }
    }
}

if (isset($_GET['list'])) {
    // make sure the directory exsits
    if (is_dir($bor_dir)) {
        // open it as a dir
        if ($dh = opendir($bor_dir)) {
            // loop through all files in the directory
            while (($file = readdir($dh)) !== false) {
                // make sure we don't search . and .. or hidden files
                if ((str_starts_with($file, ".")) !== true) {
                    echo $file . ",";
                }
            }
        }
    }
}
if (isset($_GET['getinfo'])) {
    $pkg_dir = $_GET['getinfo'];
    
    $file_loc = "./bor/";
    $file_loc .= $pkg_dir;
    // verify that the directory entered is correct
    if (is_dir($file_loc)) {
        // make a string containing the location of the info.txt file
        // get the info file
        $info_loc = $file_loc;
        $info_loc .= "/info.txt";
        
        $infofile = fopen($info_loc, "r");
        // output the file
        echo nl2br(fread($infofile, filesize($file_loc)));
        // close the file
        fclose($infofile);
    }
    
    else {
        echo 1;
    }
}
if (isset($_GET['getpath'])) {
    $pkg_dir = $_GET['getpath'];
    $file_loc = "bor/";
    $file_loc .= $pkg_dir;
    if (is_dir($file_loc)) {
        echo $file_loc;
    }
    else {
        echo 1;
    }
}


if (isset($_GET['report'])) {
    // get the package name
    $pkg_name = $_GET['report'];
    // define where the package is
    $file_loc = "bor/";
    $file_loc .= $pkg_name;
    // make sure the package actually exists
    if (is_dir($file_loc)) {
        // set the info.txt file
        $file = $file_loc; 
        $file .= "/info.txt";
        // open it
        $fh = fopen($file, "r+");
        
        // make the buffer for the file that will be written
        $buffer = '';

        // go line by line through info.txt while also keeping track of the line number
        $i = 1;
        while (!feof($fh)) {
            $data = fgets($fh);
            // only edit line when we are on line 4 (where the report number is kept) 
            if ($i == 4) {
                // remove line ending from data
                $data = trim($data);
                // convert the line into a integer
                $reportNum = (int) $data;
                // increase it by one
                $reportNum++;
                // recast as a string
                $data = (string) $reportNum;
                // re add the line ending
                $data .= "\n";
                // add it to the buffer
                $buffer .= $data;
            }
            else {
                // append current line data
                $buffer .= $data;
            }
            // increment i by one
            $i++;
        }
        // overwrite the file with the conents of buffer and then close it
        file_put_contents($file, $buffer);
        fclose($fh);
    }
    else {
        echo 1;
    }
}

if (isset($_GET['upload'])) {
    echo '
    <html>
        <body>
            <form action=bopirruu.php?rxpkg method="post" enctype="multipart/form-data">
                Zip file containing package: <input type="file" name="file"><br>
                <input type="submit" value="Upload">
            </form>
        </body>
    </html>
    ';
}
if (isset($_GET['rxpkg'])) {
    echo "1 OK<br>";
    $file = $_FILES["file"]["tmp_name"];
    
    echo "<br>";
    echo $_FILES["file"]["type"];
    echo "<br>";
    echo $_FILES["file"]["name"];
    echo "<br>";
    echo $_FILES["file"]["size"];
    // make sure that the file is a zip archive
    if ($_FILES['file']['type'] !== "application/octet-stream") {
        echo 1;
    }
    else { 
        echo "file recieved!<br>";
        $path = "./bor/";

        $ziploc = $path;
        $ziploc .= $_FILES['file']["name"];
        
        move_uploaded_file($file, $ziploc);
        echo "file downloaded!<br>";
        
        $zip = new ZipArchive;
        $res = $zip->open($ziploc);
        if ($res === TRUE) {
            $zip->extractTo($path);
            $zip->close();
            unlink($ziploc);
            echo "file uploaded!!!";
        }
        else {
            echo 2;
        }
    }
}

?>
