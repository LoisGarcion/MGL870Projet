package com.example.ProductSpringBoot.Controller;

import com.example.ProductSpringBoot.Model.ProductModel;
import com.example.ProductSpringBoot.Service.ProductService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/product")
public class ProductController {
    @Autowired
    private ProductService productService;

    @PostMapping("/create")
    public ProductModel createProduct(@RequestBody ProductModel product) {
        return productService.saveProduct(product);
    }

    @GetMapping("/all")
    public List<ProductModel> getAllProducts() {
        return productService.getAllProduct();
    }

    @GetMapping("/get/{id}")
    public ProductModel getProductById(@PathVariable Long id) {
        return productService.getProductById(id);
    }
}
