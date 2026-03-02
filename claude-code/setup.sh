#!/bin/bash

cat /root/claude-code/coop-intro.txt

cat >> /root/.bashrc << 'EOF'
cat /root/claude-code/coop-intro.txt
echo ' '
echo '================================='
EOF

exec "$@"