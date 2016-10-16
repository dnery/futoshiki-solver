package main

import "fmt"

func ptrs(x *[]float64) (res float64) {

        res = (*x)[2]
        fmt.Println(res)
        return
}


func main() {

        x := []float64{1, 2, 3, 4}
        ptrs(&x)
}
