#!/bin/bash

BUILD=false
UP=false
DOWN=false

for arg in "$@"; do
  case "$arg" in
    --build) BUILD=true ;;
    --up) UP=true ;;
    --down) DOWN=true ;;
    *) echo "Usage: ./coop.sh [--build] [--up] [--down]" ;;
  esac
done

if [ "$BUILD" = true ]; then
  docker compose -f "locollama.yml" build
fi

if [ "$UP" = true ]; then
  python3 utilities/inject-volumes.py locollama.yml --inject
  if docker compose -f "locollama.yml" up -d; then
    python3 utilities/inject-volumes.py locollama.yml --eject
    docker exec -it coop bash -c "cd /root && exec bash"
  else
    echo "docker compose up failed — compose file left with injected mounts"
  fi
fi

if [ "$DOWN" = true ]; then
  docker compose -f "locollama.yml" down
fi