#!/bin/bash
# Bash Menu Script Example

mkdir -p ~/Downloads/renders
PS3='What size asset do you want (1/2/3/4 to quit)? '
options=("300x250" "300x600" "160x600" "970x250" "Quit")
translate="n"
select opt in "${options[@]}"
do
  case $opt in
    "300x250")
      read -p "What do you want it to say (40 chars max)? " copy
      # read -p "Would you like it to be translated (y/n)? " translate
      echo "Generating assets..."
      ./dist/app.app/Contents/MacOS/app --format 300_250 --copy "$copy" --cta "$cta"
      for o in "${!options[@]}"; do echo "$((o+1)))" "${options[$o]}"; done
      ;;
    "300x600")
      read -p "What do you want it to say (105 chars max)? " copy
      # read -p "Would you like it to be translated (y/n)? " translate
      echo "Generating assets..."
      ./dist/app.app/Contents/MacOS/app --format 300_600 --copy "$copy" --cta "$cta"
      for o in "${!options[@]}"; do echo "$((o+1)))" "${options[$o]}"; done
      ;;
    "160x600")
      read -p "What should it say (140 chars max)? " copy
      read -p "What should the button say (16 chars max)? " cta
      echo "Generating assets..."
      ./dist/app.app/Contents/MacOS/app --format 160_600 --copy "$copy" --cta "$cta"
      for o in "${!options[@]}"; do echo "$((o+1)))" "${options[$o]}"; done
      ;;
    "970x250")
      read -p "What do you want it to say (140 chars max)? " copy
      # read -p "Would you like it to be translated (y/n)? " translate
      echo "Generating assets..."
      ./dist/app.app/Contents/MacOS/app --format 970_250 --copy "$copy" --cta "$cta"
      for o in "${!options[@]}"; do echo "$((o+1)))" "${options[$o]}"; done
      ;;
    "Quit")
      break
      ;;
    *) echo "invalid option $REPLY. Please enter a number e.g. 1, 2, 3";;
  esac
done
