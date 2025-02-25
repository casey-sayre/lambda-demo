#!/bin/bash

# Find all directories ending with "lambda_function".
# Each directory name matches a pyproject group name.
find src/lambda_demo -maxdepth 1 -type d -name "*_lambda_function" | while read -r dir; do
  group_name=`basename $dir`
  echo updating deps for $group_name in $dir
  poetry export --without-hashes -f requirements.txt --only $group_name --output $dir/requirements.txt
done