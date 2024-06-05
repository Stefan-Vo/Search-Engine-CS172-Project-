#!/bin/bash

# Array of inputs
inputs=("YOUR SUBREDDITS HERE")
num_posts=1000  # Default number of posts to crawl

# Check if the number of posts argument is provided
if [ $# -eq 1 ]; then
    num_posts=$1
fi

# Iterate over inputs
for input_text in "${inputs[@]}"
do
    echo "Crawling r/$input_text for $num_posts posts..."
    python3 ./crawler.py <<< "$input_text $num_posts"
    echo "Done crawling r/$input_text."
    sleep 1
done
