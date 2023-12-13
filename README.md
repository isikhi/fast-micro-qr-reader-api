# Micro QR Code Reader

## Overview

This open-source project is a Micro QR code reader application built using FastAPI and various image processing libraries.

## Purpose

The goal of this application is to provide a high-precision Micro QR code reading service. It leverages advanced image processing techniques to accurately extract information from these small and data-limited QR codes.

## Challenges of Micro QR Code Reading

Micro QR codes pose unique challenges compared to traditional QR codes due to their significantly smaller size and reduced data capacity. Challenges include accurate edge detection and optical character recognition (OCR) in a constrained space.

## Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/): A modern, high-performance web framework.
- [PyBoof](https://pypi.org/project/pyboof/): A computer vision library for Python.

## Running the Application

### Prerequisites

- Python 3.x installed on your system.
- Java(https://openjdk.org/) 8+ installed on your system. Tested with 17.x

### Install & Run (without docker/compose)

1. Clone the repository:

    ```bash
    git clone https://github.com/isikhi/fast-micro-qr-reader-api.git
    cd fast-micro-qr-reader-api
    ```

2. Install dependencies:

    ```bash
    pip install -r requirements.txt
    ```

3. Run with default port(8000)

    ```bash
    uvicorn app.main:app --reload
   ```

### Install & Run with docker
1. Clone the repository:

    ```bash
    git clone https://github.com/isikhi/fast-micro-qr-reader-api.git
    cd fast-micro-qr-reader-api
    ```

2. Build the Docker image:

    ```bash
    docker build -t fast-micro-qr-reader-api .
    ```

3. Run the Docker container

    ```bash
   docker run -p 8080:8080 fast-micro-qr-reader-api
   ```
   
### Install & Run with docker compose(Optional)
1. Build and run with Docker Compose(if you want to detach add -d flag to end):

    ```bash
   docker run -p 8080:8080 fast-micro-qr-reader-api
   ```


### Check and Test
#### Server is up? 
- Visit http://127.0.0.1:8000 in your browser to access nothing but see server is up :D
#### Curl Request for Micro QR Code Decoding
- Make sure to replace /home/isikhi/test/... with the actual paths of your image files and use curl or import to postman
```bash
curl --location 'localhost:8080/micro-qrs/decode' \
--form 'files=@"/home/isikhi/test/microqr1.png"' \
--form 'files=@"/home/isikhi/test/microqr2.png"'
```

#### HTTP Request for Micro QR Code Decoding
- Make sure to replace /home/isikhi/test/... with the actual paths of your image files and use your IDE http tool

```http
POST http://localhost:8080/micro-qrs/decode
Content-Type: multipart/form-data; boundary=--------------------------239061361532539650648925

--------------------------239061361532539650648925
Content-Disposition: form-data; name="files"; filename="/home/isikhi/test/microqr1.png"
Content-Type: image/png

<@/home/isikhi/test/microqr1.png
--------------------------239061361532539650648925
Content-Disposition: form-data; name="files"; filename="/home/isikhi/test/microqr2.png"
Content-Type: image/png

<@/home/isikhi/test/microqr2.png
--------------------------239061361532539650648925--
