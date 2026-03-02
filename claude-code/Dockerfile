FROM node:20-slim

# Install dependencies
RUN apt-get update && apt-get install -y curl git vim ca-certificates openssh-client vim python3-pip
RUN apt install -y python3 python3-pip 

# Install claude code
RUN curl -fsSL https://claude.ai/install.sh | bash

#Install lasso prompt-injection-defender
RUN git clone https://github.com/lasso-security/claude-hooks.git /root/claude-hooks
RUN chmod +x /root/claude-hooks/install.sh
RUN /root/claude-hooks/install.sh /root/

#setup PATH for claude
RUN echo 'export PATH="/root/.local/bin:$PATH"' >> /root/.bashrc

#setup 
RUN mkdir -p /root/claude-code
COPY ./coop-intro.txt /root/claude-code
COPY ./setup.sh /root/claude-code
COPY ./test-lasso.txt /root/claude-code
RUN chmod +x /root/claude-code/setup.sh
ENTRYPOINT ["/root/claude-code/setup.sh"]
CMD ["bash"]