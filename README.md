# Summary
Revisiting an old project I did to solve mazes using various graph-traversal methods. Updating by adding more types and functionality.  

# How it works  
Runs by command line. An example run would be

`python3 main.py input.txt`  

With input.txt having the following format. A sample input is included.

```
start(0,0)
end(0,6)
0 9 9 9 9 9 0
1 1 1 1 1 9 1
1 9 9 9 1 9 1
1 9 9 1 1 9 1
1 1 1 1 1 1 1
```

Output is a `output.txt` file with various statistics such as time taken to compute, memory used, nodes explored, and path length.

# Recreation

Clone the repo locally.  

Make your way to the directory.

`python3 -m venv venv`  
`source venv/bin/activate`
`pip install -r requirements.txt`