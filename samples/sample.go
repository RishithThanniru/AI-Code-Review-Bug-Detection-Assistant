package main

import "fmt"

type Point struct {
	X int
	Y int
}

func add(a int, b int) int {
	return a + b
}

func printPoints(points []Point) {
	for _, p := range points {
		if p.X > 0 {
			fmt.Println(p.X, p.Y)
		}
	}
}

func main() {
	fmt.Println(add(2, 3))
}
