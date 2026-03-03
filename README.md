       /\~~/\
       \ -_-/
        ""v"              

Welcome to Coop -_-

This is a sandbox for Claude Code
with prompt-injection detection 

V1.0:
Allows you to spin up Claude Code in a containerized and isolated environment that out-of-the-box has prompt injection detection from [@Lasso](https://github.com/lasso-security/claude-hooks) configured. Claude Code can't see any files on your personal machine unless you grant access by specifying the file paths in custom-volumes.txt 

Setup:
1) Install required softwares
- [Docker](https://www.docker.com/get-started/)
- [Ollama](https://ollama.com/download)
- [Python3](https://www.python.org/downloads/)

2) python3 -m pip install pyyaml

3) Ollama Setup

    a) Download one of the [recommended models](https://docs.ollama.com/integrations/claude-code#recommended-models) for Claude Code.

    b) Adjust [context length](https://docs.ollama.com/context-length). Recommended to set to at least 32k for Claude Code.

    c) ollama run <model>
    - coop will use the locally running instance of Ollama 

4) Coop Setup

    a) vi .env
        - CLAUDE=<path_to_.claude>
        - mount this directory so that session history can be persisted 

    b) vi custom-volumes.txt
        - add paths to any directories you want Claude Code to have access to. 
        - the directories are added to the docker compose before bringup and removed once bringup is done.

    c) chmod +x ./coop.sh

    d) ./coop.sh 
        --build : builds the sandbox / container
        --up    : brings up the container, logs you into the shell
        --down  : brings down the container

    e) claude --model <model running in Ollama>
        - launch Claude Code in the sandbox 


<img width="904" height="748" alt="image" src="https://github.com/user-attachments/assets/965046d1-8484-436d-a733-e425b50e2a01" />


*Testing the prompt-injection detection from Lasso
<img width="1274" height="1708" alt="image" src="https://github.com/user-attachments/assets/889f9720-67f0-4293-9258-d63f69955338" />


Next Steps:
- introduce support for OpenClaw
- introduce multi-container setup to run multiple agents in truly isolated environments
