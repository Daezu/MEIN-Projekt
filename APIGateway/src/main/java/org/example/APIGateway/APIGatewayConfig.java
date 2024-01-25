package org.example.APIGateway;

import org.springframework.cloud.gateway.route.RouteLocator;
import org.springframework.cloud.gateway.route.builder.RouteLocatorBuilder;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

@Configuration
public class APIGatewayConfig {
        @Bean
        public RouteLocator gatewayRoutes(RouteLocatorBuilder builder) {
                return builder.routes() // keep the order, it is significant
                                // UserService route
                                .route("UserService", r -> r.path("/**")
                                                .uri("http://user-service:8081"))
                                .build();
        }
}