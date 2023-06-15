#!/bin/bash

while getopts "f:" opt; do
  case $opt in
    f)
      file_path=$OPTARG
      ;;
    \?)
      echo "Opção inválida: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Opção -$OPTARG requer um argumento." >&2
      exit 1
      ;;
  esac
done

if [ -z "$file_path" ]; then
  echo "Por favor, especifique o arquivo usando a opção -f."
  exit 1
fi

if [ -f "$file_path" ]; then
  formatted_content=$(sed ':a;N;$!ba;s/\n/\\n/g' "$file_path")
  echo "$formatted_content"
else
  echo "Arquivo não encontrado: $file_path"
  exit 1
fi
