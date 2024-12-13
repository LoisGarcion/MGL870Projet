package com.example.ProductSpringBoot.Service;

import com.example.ProductSpringBoot.Model.ProductModel;
import com.example.ProductSpringBoot.Controller.ProductController;
import com.example.ProductSpringBoot.Repository.ProductRepository;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.slf4j.event.Level;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.List;

@Service
public class ProductService {
    private static final Logger log = LoggerFactory.getLogger(ProductService.class);
    @Autowired
    private ProductRepository productRepository;

    public ProductModel saveProduct(ProductModel product) {
        log.info("Saving product");
        return productRepository.save(product);
    }

    public List<ProductModel> getAllProduct() {
        log.info("Getting all users");
        return productRepository.findAll();
    }

    public ProductModel getProductById(Long id) {
        log.info("Getting product by id");
        return productRepository.findById(id).orElse(null);
    }
}
