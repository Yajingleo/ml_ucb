package main
import ("fmt")

func myFunction(x int, y int) int {
  return x + y
}

type User struct {
	name string
	age int
}

func (p *User) Str() string {
	return fmt.Sprintf("Hi, I'm %s, %d years old", p.name, p.age)
}


func main() {
  var p User = User{name: "Bob", age: 32}
  fmt.Println(p.Str())

  fmt.Println(myFunction(1, 2))

  const PI = 3.14

  var a bool = true     // Boolean
  var b int = 5         // Integer
  var c float32 = 3.14  // Floating point number
  var d string = "Hi!"  // String

  fmt.Println("Boolean: ", a)
  fmt.Println("Integer: ", b)
  fmt.Println("Float:   ", c)
  fmt.Println("String:  ", d)

  var array_1 = [5]int{1, 2, 3, 4, 5}
  var array_2 = [...]int{1, 2, 3, 4, 5}
  array_3 := [...]int{1, 2, 3, 4, 5}
  fmt.Println(array_1)
  fmt.Println(array_2)
  fmt.Println(array_3)

  myslice1 := []int{}
  fmt.Println(len(myslice1))
  fmt.Println(cap(myslice1))
  fmt.Println(myslice1)

  myslice2 := []string{"Go", "Slices", "Are", "Powerful"}
  fmt.Println(len(myslice2))
  fmt.Println(cap(myslice2))
  fmt.Println(myslice2)
}