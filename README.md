  
# Simple Spring Boot with Docker Application#


Build the image using the following command

```bash
$ docker build -t docker_springboot_demo .
```
Run the Docker container using the command shown below.

```bash
$ docker run -d -p 8080:8080 docker-springboot_demo
```

The application will be accessible at http://localhost:8080/

