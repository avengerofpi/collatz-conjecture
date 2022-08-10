#!/bin/bash

set -eu

batchSize=100;
numBatches=5;
for iStart in $(seq 0 $((numBatches - 1))); do
  batchStart=$((${iStart} * ${batchSize}));
  batchEnd=$(((${iStart} + 1) * ${batchSize}));
  startValues="$(python3 -c "print(tuple(2 ** i -1 for i in range( ${batchStart}, ${batchEnd} + 1 )))")"
  echo "Batch ${iStart}: range ${batchStart} to ${batchEnd}";
  for db in data/collatz.{01..03}.db; do
    echo "$(sqlite3 "${db}" "SELECT start, startBitLen, pathLen FROM PathDetails WHERE start IN ${startValues}" | md5sum) ${db}";
  done;
  echo
done
