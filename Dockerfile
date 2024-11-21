FROM openjdk:17
MAINTAINER "Ramadevi"
COPY target/spring-boot-docker-app.jar  spring-boot-docker-app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "spring-boot-docker-app.jar"]
