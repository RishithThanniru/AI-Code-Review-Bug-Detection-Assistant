import { readFile } from "fs";

class Calculator {
    add(a, b) {
        return a + b;
    }

    multiply(a, b) {
        return a * b;
    }
}

function processItems(items) {
    for (let i = 0; i < items.length; i++) {
        if (items[i] > 0) {
            console.log(items[i]);
        }
    }
}

const calc = new Calculator();
console.log(calc.add(2, 3));
