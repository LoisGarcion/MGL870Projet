# Use a Maven image to build the application
FROM maven:3.9.5-eclipse-temurin-17 as builder
WORKDIR /app
COPY . .
RUN mvn clean package -DskipTests

# Use a lightweight Java image to run the application
FROM eclipse-temurin:17-jdk
WORKDIR /app

# Copy the application JAR
COPY --from=builder /app/target/UserSpringBoot-0.0.1-SNAPSHOT.jar app.jar

# Copy the OpenTelemetry Java agent from your project directory
COPY src/main/otlpjavaagent/opentelemetry-javaagent.jar /otel-agent.jar

# Add OpenTelemetry configuration file (optional)
COPY src/main/otlpjavaagent/otel.properties /app/otel.properties

# Expose application port
EXPOSE 8080

# Run the application with the agent
ENTRYPOINT ["java", "-javaagent:/otel-agent.jar", \
            "-Dotel.javaagent.configuration-file=/app/otel.properties", \
            "-jar", "app.jar"]
