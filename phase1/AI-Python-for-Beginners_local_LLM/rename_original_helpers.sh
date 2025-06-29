#!/bin/bash

# Define the target parent folders
PARENT_FOLDERS=(
  "3_Working with Your Own Data and Documents in Python"
  "4_Extending Python with Packages and APIs"
)

# Loop through each parent folder
for parent in "${PARENT_FOLDERS[@]}"; do
  echo "Checking in: $parent"
  
  # Loop through subfolders L1 to L7
  for i in {1..7}; do
    subfolder="$parent/L$i"
    old_file="$subfolder/helper_functions.py"
    new_file="$subfolder/helper_functions-openai.py"

    # Check and rename if file exists
    if [[ -f "$old_file" ]]; then
      echo "Renaming: $old_file -> $new_file"
      mv "$old_file" "$new_file"
    else
      echo "No file found at: $old_file"
    fi
  done
done
