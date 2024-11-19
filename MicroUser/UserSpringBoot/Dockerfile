# Use a Maven image to build the application
FROM maven:3.9.5-eclipse-temurin-17 as builder
WORKDIR /app
COPY . .
RUN mvn clean package -DskipTests

# Use a lightweight Java image to run the application
FROM eclipse-temurin:17-jdk
WORKDIR /app
COPY --from=builder /app/target/UserSpringBoot-0.0.1-SNAPSHOT.jar app.jar
EXPOSE 8080
ENTRYPOINT ["java", "-jar", "app.jar"]
