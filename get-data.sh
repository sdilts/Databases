#!/bin/bash
files=("name.basics.tsv.gz" "title.akas.tsv.gz" "title.basics.tsv.gz" "title.crew.tsv.gz" \
	"title.episode.tsv.gz" "title.principals.tsv.gz" "title.ratings.tsv.gz")

mkdir data
cd data

for file in "${files[@]}"
do
	echo "Processing file $file"
	curl -O "https://datasets.imdbws.com/$file"
	gzip -d $file
	echo ""
done
