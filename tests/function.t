% Function to calculate the factorial of a number
function factorial(n: int) : real
    if n = 0 then
        result 1
    else
        result n * factorial(n - 1)
    end if
end factorial

factorial(5)