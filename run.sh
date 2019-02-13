#!/bin/bash
# Bash Menu Script Example

source cv-py3/bin/activate
PS3='Please input dimensions for output: '
options=("300x250" "300x600" "970x250" "Quit")
select opt in "${options[@]}"
do
  case $opt in
    "300x250")
      echo "Generating assets..."
      python3 app.py --format 300_250
      ;;
    "300x600")
      echo "Generating assets..."
      python3 app.py --format 300_600 
      ;;
    "970x250")
      echo "Generating assets..."
      python3 app.py --format 970_250
      ;;
    "970x250")
      echo "Generating assets..."
      python3 app.py --format 970_250
      ;;
    "Quit")
      break
      ;;
    *) echo "invalid option $REPLY. Please enter a number e.g. 1, 2, 3";;
  esac
done
