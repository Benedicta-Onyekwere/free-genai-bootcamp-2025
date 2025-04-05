#! /bin/bash

echo "Get ready to record in..."
for i in 3 2 1
do
    echo "$i..."
    sleep 1
done
echo "START RECORDING NOW!"
echo "Recording for 10 seconds..."

for i in {1..10}
do
    echo -n "."
    sleep 1
done

echo -e "\nSTOP RECORDING NOW!" 