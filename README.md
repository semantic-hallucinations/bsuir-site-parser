# BSUIR website parser

This parser scrap info from all pages on bsuir.by website except some dropped topics

## Dropped topics

Some topics that we thing are not valuable in our opinion are skipped. We also collect links to files within the site in some extensions. You can find out about dropped/saved themes and extensions in limits directory.

## Data loader

This parser loads data to local storage or send content to other service, it's resolving using .env configuration.

To set up remote config provide
```DATA_LOADER_URL```
OR
```
DATA_LOADER_NAME
DATA_LOADER_PORT
DATA_LOADER_ENDPOINT
```

To set up local loader just don't configurate remote config and provide directory for files ```DATA_STORAGE_DIR``` (this also require to use volume for local data storage)

## Using docker image
```
services:
  bsuir-parser:
    image: ghcr.io/semantic-hallucinations/bsuir-site-parser:latest
    env_file:
      - .env
    volumes:
      - ./data:/app/data    # only if you ran for local storaging in md files              # only if you store data in directory, else delete volumes
    command: [ "python", "main.py" ]
```
