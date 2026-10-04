#!/usr/bin/env bash


echo 
echo "git starting ......"
echo 

# Vérifier qu'un paramètre est passé
if [ -z "$1" ]; then
  echo "Usage: ./git.sh <parametre>"
  exit 1
fi

PARAM="$1"

echo "Adding file : $PARAM ...  "
echo 
echo 
# Exemple 1 : ajouter tous les fichiers modifiés
git add .

echo "Commiting  file : $PARAM ...."
echo 
# Commit avec message personnalisé
git commit -m "add modifications $PARAM  $(date '+%Y-%m-%d %H:%M:%S') "
echo "Commit OK!"
echo 
echo 

echo "Pushing file : $PARAM ... $(date '+%Y-%m-%d %H:%M:%S') "
echo 
# Push
git push

echo 
echo "git ok!"