# Loading Image
FROM ubuntu:22.04 
LABEL author="Dasun Gunasinghe <dasun.gunasinghe@qut.edu.au>"

# Define user params
ARG USER=ubuntu
ENV USER=${USER}

# Update apt-get and give user sudo privileges
RUN apt-get update && apt-get install -y sudo && \
  adduser --disabled-password --gecos "" ${USER} && \
  echo "${USER} ALL=(ALL) NOPASSWD: ALL" >> /etc/sudoers

# User defines continued (post sudo)
USER ${USER}
WORKDIR /home/${USER}
SHELL ["/bin/bash", "-c"]

# Install pip and other packages 
RUN sudo apt-get install -y python3-pip 

# Install any general requirements
COPY ./requirements.txt /home/${USER}/requirements.txt
RUN pip install -r /home/${USER}/requirements.txt

# Copy the entry point in 
COPY ./entrypoint.sh /usr/local/bin/entrypoint
RUN sudo chmod +x /usr/local/bin/entrypoint
ENTRYPOINT ["/usr/local/bin/entrypoint"]
CMD ["bash"]
