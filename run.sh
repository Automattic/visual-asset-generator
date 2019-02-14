#!/bin/bash
# Bash Menu Script Example

source cv-py3/bin/activate
echo "Hello!"
PS3='What size asset do you want? (1/2/3/4): '
options=("300x250" "300x600" "970x250" "Quit")
select opt in "${options[@]}"
do
  case $opt in
    "300x250")
      read -p "What do you want it to say? (40 character limit): " fullname
      echo "Generating assets..."
      python3 app.py --format 300_250 --copy "$fullname"
      open outputs/renders
      ;;
    "300x600")
      echo "Generating assets..."
      python3 app.py --format 300_600 --copy "$fullname"
      open outputs/renders
      ;;
    "970x250")
      echo "Generating assets..."
      python3 app.py --format 970_250 --copy "$fullname"
      open outputs/renders
      ;;
    "Quit")
      break
      ;;
    *) echo "invalid option $REPLY. Please enter a number e.g. 1, 2, 3";;
  esac
done
