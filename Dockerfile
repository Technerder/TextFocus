FROM ubuntu:20.04 AS builder-image

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3.9-dev python3.9-venv python3-pip python3-wheel build-essential && apt-get clean && rm -rf /var/lib/apt/lists/*

# create and activate virtual environment using final folder name to avoid path issues with packages
RUN python3.9 -m venv /home/textfocususer/venv
ENV PATH="/home/textfocususer/venv/bin:$PATH"

# install requirements
COPY src/requirements.txt .
RUN pip3 install --no-cache-dir wheel
RUN pip3 install --no-cache-dir -r requirements.txt

FROM ubuntu:20.04 AS runner-image
RUN apt-get update && apt-get install --no-install-recommends -y python3.9 python3-venv && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN useradd --create-home textfocususer
COPY --from=builder-image /home/textfocususer/venv /home/textfocususer/venv

USER textfocususer
RUN mkdir -p /home/textfocususer/ && chown textfocususer /home/textfocususer/
WORKDIR /home/textfocususer/
COPY src .

# make sure all messages always reach console
ENV PYTHONUNBUFFERED=1

# activate virtual environment
ENV VIRTUAL_ENV=/home/textfocususer/venv
ENV PATH="/home/textfocususer/venv/bin:$PATH"

CMD ["python", "main.py"]