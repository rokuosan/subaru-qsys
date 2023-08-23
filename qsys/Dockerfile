FROM python:3.11.4

ARG UID=1000
ARG GID=1000
ARG USERNAME=django
ARG GROUPNAME=django

RUN groupadd -g $GID $GROUPNAME && \
    useradd -u $UID -g $GID -m $USERNAME

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt && pip install uwsgi

# COPY entrypoint.sh /usr/local/bin/entrypoint.sh
# RUN apt-get update && apt-get -y install gosu && \
#     chmod +x /usr/local/bin/entrypoint.sh
# ENTRYPOINT [ "/usr/local/bin/entrypoint.sh" ]

# Run entrypoint.sh
CMD ["/bin/bash", "entrypoint.sh"]
