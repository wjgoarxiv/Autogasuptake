#!/bin/bash
# advanced.sh
for filenum in 0 2 4 6
do
  autogasuptake << EOF
  $filenum
    50
EOF
done