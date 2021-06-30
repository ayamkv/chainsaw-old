FROM       python
RUN        pip install -r /path/to/requirements.txt
COPY       . /app
WORKDIR    /
RUN        echo "installing stuff?"
ENV        SHELL=/bin/bash
CMD        ["python"]