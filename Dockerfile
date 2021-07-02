FROM       python
RUN        mkdir -p /user/src/app
WORKDIR    /user/src/app
COPY       requirements.txt ./
COPY       . .
RUN        pip install -r requirements.txt
RUN        echo "installing stuff?"
# ENV        SHELL=/bin/bash
CMD        ["python, app.py"]