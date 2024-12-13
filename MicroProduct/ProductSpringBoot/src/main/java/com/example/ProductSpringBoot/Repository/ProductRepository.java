package com.example.ProductSpringBoot.Repository;

import com.example.ProductSpringBoot.Model.ProductModel;
import org.springframework.data.jpa.repository.JpaRepository;

public interface ProductRepository extends JpaRepository<ProductModel, Long> {
}
