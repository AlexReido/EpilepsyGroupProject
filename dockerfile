FROM python:latest
RUN mkdir /app
ADD ./ /app/
RUN pip install --upgrade pip
RUN yes | apt-get update
RUN yes | apt-get install software-properties-common
RUN wget --no-check-certificate -O - https://apt.llvm.org/llvm-snapshot.gpg.key | apt-key add -
RUN add-apt-repository 'deb http://apt.llvm.org/bionic/   llvm-toolchain-bionic-10  main'
RUN apt update
RUN yes | apt-get install llvm-10*
RUN ln -s /usr/bin/llvm-config-10 /usr/bin/llvm-config
RUN pip install numba --user
RUN pip install -r app/requirements.txt
ENV PYTHONPATH "${PYTHONPATH}:/app/"
WORKDIR /app/PythonCode/TyperCLI
EXPOSE 8888
CMD ["python", "/app/PythonCode/TyperCLI/TyperSearch.py"]