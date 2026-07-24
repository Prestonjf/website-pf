#!/bin/bash
set -e

SERVICE=website-react-pf-webapp
USAGE='usage: deploy.sh <stage>'
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

CONFIG_FILE="$SCRIPT_DIR/../../sonar-project.properties"
VERSION=$(sed -n 's/^sonar.projectVersion=//p' "$CONFIG_FILE")

if [ $# -lt 1 ]; then
    echo "$USAGE"
    echo '(You forgot to put a stage!)'
    exit 1
fi

echo "Deploying $SERVICE-webapp to ${1}!"

# build webapp .env file
poetry run python3 ./create_webapp_config.py $1

# build webapp
export NODE_OPTIONS=--openssl-legacy-provider
npm run-script build

# Remove old webapp
aws s3 rm s3://website-pf-webapp-$1/ --recursive

# Upload new webapp
aws s3 cp build/ s3://website-pf-webapp-$1/site/$VERSION/ --recursive --cache-control max-age=31536000,s-maxage=2592000

upload_if_missing() {
    local stage="$1"
    local source_path="$2"
    local target_key="$3"
    local cache_control="$4"

    if aws s3api head-object --bucket "website-pf-content-$stage" --key "$target_key" >/dev/null 2>&1; then
        echo "Skipping existing object: $target_key"
    else
        aws s3 cp "$source_path" "s3://website-pf-content-$stage/$target_key" --cache-control "$cache_control"
    fi
}

# Upload webapp config content
upload_if_missing "$1" "config/robots.txt" "config/robots.txt" "max-age=86400,s-maxage=86400"
upload_if_missing "$1" "config/rss.xml" "config/rss.xml" "max-age=86400,s-maxage=86400"
upload_if_missing "$1" "config/featured.yml" "config/featured.yml" "max-age=0,s-maxage=0"
upload_if_missing "$1" "config/sitemap.xml" "config/sitemap.xml" "max-age=86400,s-maxage=86400"
upload_if_missing "$1" "config/privacypolicy.html" "config/privacypolicy.html" "max-age=31536000,s-maxage=2592000"

# Upload webapp media content
upload_if_missing "$1" "media/homepage.jpg" "media/homepage.jpg" "max-age=31536000,s-maxage=2592000"
upload_if_missing "$1" "media/post-logo.png" "media/post-logo.png" "max-age=31536000,s-maxage=2592000"
upload_if_missing "$1" "media/post-logo-alt.png" "media/post-logo-alt.png" "max-age=31536000,s-maxage=2592000"

# Upload webapp initial posts content
upload_if_missing "$1" "posts/about/config.yml" "posts/about/config.yml" "max-age=31536000,s-maxage=2592000"
