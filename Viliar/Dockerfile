ARG dockerImage
FROM ${dockerImage} as base

ENV HOME /root
ENV PYTHONPATH=${HOME}
ENV USER python
ENV PYTHONUNBUFFERED=1
ENV HOST=${HOST}
ENV PORT=${PORT}
ENV DEBUG=${DEBUG}
RUN adduser --system --no-create-home python
WORKDIR /app
#USER python


# Install necessary packages
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    libpq-dev \
    python3-dev \
    gcc && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Install psycopg2
RUN pip install psycopg2

# -----------------------------
# LAYER 1 CUSTOMIZATIONS
# -----------------------------

FROM base as layer1

# Define build arguments and environment variables
ARG projectHomeDirpath
ARG packagename
ENV PACKAGE_NAME=${packagename}
ENV PACKAGE_DIR=${HOME}/${PACKAGE_NAME}
RUN mkdir -p ${PACKAGE_DIR}

COPY ${projectHomeDirpath}requirements.txt ${PACKAGE_DIR}/requirements.txt

RUN pip3 install --no-cache-dir -r ${PACKAGE_DIR}/requirements.txt

# Copy application files

COPY ${projectHomeDirpath}migrations ${PACKAGE_DIR}/migrations
COPY ${projectHomeDirpath}alembic.ini ${PACKAGE_DIR}/alembic.ini
COPY ${projectHomeDirpath}src ${PACKAGE_DIR}/src
COPY ${projectHomeDirpath}app.py ${PACKAGE_DIR}/app.py
COPY ${projectHomeDirpath}factory.py ${PACKAGE_DIR}/factory.py
COPY ${projectHomeDirpath}utils.py ${PACKAGE_DIR}/utils.py
COPY ${projectHomeDirpath}__init__.py ${PACKAGE_DIR}/__init__.py

# entrypoint
COPY ${projectHomeDirpath}entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Set the entrypoint
ENTRYPOINT [ "/entrypoint.sh"]
CMD [ "tail", "-f", "/dev/null"]
