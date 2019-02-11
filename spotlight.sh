#!/bin/bash
# Bash Menu Script Example

source cv-py3/bin/activate
PS3='Please select a format: '
options=("300 x 250" "300 x 600" "970 x 250" "Quit")
select opt in "${options[@]}"
do
  case $opt in
    "300 x 250")
      echo "Generating assets..."
      python3 spotlight.py --format 300_250
      ;;
    "Option 2")
      echo "you chose choice 2"
      ;;
    "Option 3")
      echo "you chose choice $REPLY which is $opt"
      ;;
    "Quit")
      break
      ;;
    *) echo "invalid option $REPLY";;
  esac
done

