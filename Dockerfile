FROM python:3.9-bullseye

WORKDIR /usr/src/app

RUN curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs |  bash -s -- -y 
ENV PATH="/root/.cargo/bin:${PATH}"

COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
