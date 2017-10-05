package main

import "fmt"
import "io/ioutil"
import "strings"

func main() {
	fData, err := ioutil.ReadFile("quotes.txt")  // read in the external file
    if err != nil {
        fmt.Println("Err is ", err)     // print any error
    }
	print("start\n")
    strbuffer := string(fData)  // convert read in file to a string
	print("0\n")

    arr := strings.Split(strbuffer, "\n")

	print("1\n")
	var somearray [2e5]string
	print("2\n")
    for i, quote := range arr {
		tmp := strings.Split(quote, " ")
		if len(tmp) > 3 {
			asdf := tmp[2] + tmp[0] + tmp[1]
			if i % 250 == 0 {
				somearray[i / 250] = asdf
			}
		}
	}
	print("3\n")
}

