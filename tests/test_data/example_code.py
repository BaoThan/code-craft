"""
This file contains strings of hello world code for multiple programming languages.
These strings will be used for testing purposes.
"""

C_HELLO_WORLD = """
#include <stdio.h>

int main() {
    printf("Hello, world!\\n");
    return 0;
}
"""

CPP_HELLO_WORLD = """
#include <iostream>

int main() {
    std::cout << "Hello, world!" << std::endl;
    return 0;
}
"""

C_SHARP_HELLO_WORLD = """
// Hello World! program
namespace HelloWorld
{
    class Hello {
        static void Main(string[] args)
        {
            System.Console.WriteLine("Hello, world!");
        }
    }
}
"""

JAVA_HELLO_WORLD = """
public class Main {
    public static void main(String[] args) {
        System.out.println("Hello, world!");
    }
}
"""

JAVASCRIPT_HELLO_WORLD = 'console.log("Hello, world!");'

PYTHON_HELLO_WORLD = 'print("Hello, world!")'

RUBY_HELLO_WORLD = 'puts "Hello, world!\\n"'

PHP_HELLO_WORLD = """<?php
  echo "Hello, world!\\n";
?>"""

RUST_HELLO_WORLD = """
fn main() {
    println!("Hello, world!");
}"""

PERL_HELLO_WORLD = """
use strict;
use warnings;

print("Hello, world!\\n");"""

GO_HELLO_WORLD = """
package main
import "fmt"
func main() {
    fmt.Println("Hello, world!")
}"""
