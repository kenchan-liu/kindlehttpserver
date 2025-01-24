#!/bin/bash
# Simple HTTP file server with basic HTML frontend using nc
root_dir="/mnt/c/Users/kentl/kindleserv"
port=8080

while true; do
  request=$(nc -l -p $port -q 1)
  url_path=$(echo "$request" | grep GET | awk '{print $2}')
  echo "Request: $url_path"
  case "$url_path" in
    /)
      file_list=$(ls -p "$root_dir" | grep -v / | awk '{print "<a href=\"/"$0"\">"$0"</a><br>"}')
      echo -e "HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>File List</h1>$file_list</body></html>" | nc -l -p $port -q 1
      ;;
    /*)
      echo "Requested file: $url_path"
      file_path="$root_dir${url_path}"
      if [ -f "$file_path" ]; then
        file_content=$(cat "$file_path")
        echo -e "HTTP/1.1 200 OK\r\nContent-Type: application/octet-stream\r\nContent-Disposition: attachment; filename=\"$(basename $file_path)\"\r\n\r\n$file_content" | nc -l -p $port -q 1
      else
        echo -e "HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1></body></html>" | nc -l -p $port -q 1
      fi
      ;;
  esac
done

