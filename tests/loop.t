var n: int := 0

loop
    exit when n >= 10
    loop
        exit when n >= 5
        put "Hello from ", n
        n := n + 1
    end loop

    put "Hello World from ", n
    n := n + 1
end loop