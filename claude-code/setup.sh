#!/bin/bash

python3 /root/claude-code/setup-hooks.py

cat /root/claude-code/coop-intro.txt

cat >> /root/.bashrc << 'EOF'
cat /root/claude-code/coop-intro.txt
echo ' '
echo '================================='
EOF

exec "$@"