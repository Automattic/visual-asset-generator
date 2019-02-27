#!/bin/bash
# Bash Menu Script Example

source cv-py3/bin/activate
PS3='What size asset do you want (1/2/3/4 to quit)? '
options=("300x250" "300x600" "160x600" "970x250" "Quit")
select opt in "${options[@]}"
do
  case $opt in
    "300x250")
      read -p "What should it say (40 chars max)? " copy
      read -p "What should the button say (16 chars max)? " cta
      echo "Generating assets..."
      python3 app.py --format 300_250 --copy "$copy" --cta "$cta"
      for o in "${!options[@]}"; do echo "$((o+1)))" "${options[$o]}"; done
      ;;
    "300x600")
      read -p "What should it say (40 chars max)? " copy
      read -p "What should the button say (16 chars max)? " cta
      echo "Generating assets..."
      python3 app.py --format 300_600 --copy "$copy" --cta "$cta"
      for o in "${!options[@]}"; do echo "$((o+1)))" "${options[$o]}"; done
      ;;
    "160x600")
      read -p "What should it say (40 chars max)? " copy
      read -p "What should the button say (16 chars max)? " cta
      echo "Generating assets..."
      python3 app.py --format 160_600 --copy "$copy" --cta "$cta"
      for o in "${!options[@]}"; do echo "$((o+1)))" "${options[$o]}"; done
      ;;
    "970x250")
      read -p "What should it say (40 chars max)? " copy
      read -p "What should the button say (16 chars max)? " cta
      echo "Generating assets..."
      python3 app.py --format 970_250 --copy "$copy" --cta "$cta"
      for o in "${!options[@]}"; do echo "$((o+1)))" "${options[$o]}"; done
      ;;
    "Quit")
      break
      ;;
    *) echo "invalid option $REPLY. Please enter a number e.g. 1, 2, 3";;
  esac
done
