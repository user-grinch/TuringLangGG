% Function to calculate the factorial of a number
% function factorial(n: int) : real
%     if n = 0 then
%         result 1
%     else
%         result n * factorial(n - 1)
%     end if
% end factorial

% Print basic outputs and test variables
put "Hello World"
put "Hello World without comments"

% Declare and initialize variables
var n: int := 0
var test: real := 5.5
var state: boolean := true
var name: string := "Hello"

loop
    loop
        exit when n > 5
        put "Hello from ", n
        n := n + 1
    end loop

    put "Hello World from ", n
    n := n + 1
    exit when n > 10
end loop

if n > 0 then
    if n > 10 then
        put "The number is greater than 10."
    else
        put "The number is less than or equal to 10."
    end if
elsif n = 0 then
    put "The number is zero."
else
    put "The number is negative."
end if

if name = "Hello" then
    put "The name is valid."
end if

% Print the values of variables
put "The value of n is ", n, ", state is ", state, ", test is ", test, ", name is ", name 

% Perform arithmetic operations and print results
n := 5
put "Updated value of n: ", n
n := (n + 10) * 2
put "Result after calculation: ", n
% Factorial calculation (uncomment to test when function is implemented)
% put "The factorial of ", n, " is ", factorial(n)