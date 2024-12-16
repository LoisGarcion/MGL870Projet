package com.example.ProductSpringBoot.Controller;

import com.example.ProductSpringBoot.Model.ProductModel;
import com.example.ProductSpringBoot.Service.ProductService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/product")
public class ProductController {
    private static final Logger log = LoggerFactory.getLogger(ProductController.class);
    @Autowired
    private ProductService productService;

    @PostMapping("/create")
    public ProductModel createProduct(@RequestBody ProductModel product) {
        log.info("POST /api/product/create Name : {}", product.getProductName());
        return productService.saveProduct(product);
    }

    @GetMapping("/all")
    public List<ProductModel> getAllProducts() {
        log.info("GET /api/product/all");
        return productService.getAllProduct();
    }

    @GetMapping("/get/{id}")
    public ProductModel getProductById(@PathVariable Long id) {
        log.info("GET /api/product/get/{}", id);
        return productService.getProductById(id);
    }
}
