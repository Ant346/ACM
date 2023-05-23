#!/bin/bash
parent_path=$( cd "$(dirname "${BASH_SOURCE[0]}")" ; pwd -P )

cd "$parent_path"

aws s3 cp --endpoint-url=https://storage.yandexcloud.net ../docs s3://rcognita --exclude '*.css' --recursive
aws s3 cp --endpoint-url=https://storage.yandexcloud.net ../docs s3://rcognita --exclude '*' --include '*.css' --no-guess-mime-type --content-type="text/css" --metadata-directive="REPLACE" --recursive


