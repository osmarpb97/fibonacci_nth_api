# Fibonacci NTH number API!

There is a lot of research about this algorithm, so I think it is a very common algorithm when we started programming (it made me remember my first semester in college) remembering how this algorithm was solved in a common way in python. 

def Fibonacci(n):

    if n == 0:
        return 0
    if n == 1:
        return 1
    else:
        return Fibonacci(n-1) + Fibonacci(n-2)

Where you had the professor explaining your first recursion classes and the advantages of recursion. But what is the problem with that algorithm in the context of what we want? Well the main problem is that we are storing all the values from the first number to the number N plus the complexity of handling the state of each of the new instances of that function! So of course if we want an efficient algorithm this is not a solution! And if we can generate a stack overflow! Like my bestfriend page!

To reduce the complexity of having to calculate all the numbers we can always resort to memoization, ie store somewhere the numbers already calculated by our api for example a non-relational database Why not relational? Because we are simply using key - value pairs and this type of database is more suitable! so we can reduce the amount of operation that our algorithm performs, so if we have already calculated the first 1000 numbers, there is no need to recalculate them, and if we have not yet arrived to calculate for example the number 2000 we would not start from 0 but from the last one, if not we would start from the sum of the last two first to calculate the next number and so on until we meet our goal. 

But that is not the objective of the proposed problem (at least that's what I want to think).

So here we start thinking, with a very basic concept of APIs! JUST BRING THE DATA YOU NEED so in this algorithm what do I really need?

F(n)=F(n-1)+F(n-2)

As we see in the formula what we need to calculate the Fibonacci number at position n is only the last 2 numbers calculated! so why keep all the previous ones? Then we implement it as follows

1.- We define the base case in line 1 
2.- Iterate up to n
3.- And we assign n-1 (n1) as n-2 (n2) also we calculate the new fibonacci number and assign it to n-2 so we only traverse one position and recalculate the value at the end the value number n will be stored in n-1 (n1)

def Fibonacci(n):

     n1, n2 = 0, 1
     for _ in range(n):
         n1, n2 = n2, n1+n2
     return n1

So very well now we have eliminated 
1.- The complexity of the compiler to handle the recursion. 2.
2.- The amount of memory used to store all the unnecessary numbers. 

So yes, this was my last implementation doing a kata in codewars!
So yes it's a good solution, but we still haven't reached the tip of the iceberg.
What else can we do?

One of the concepts I have learned solving this kind of (numerical) algorithms is that mathematical researchers almost always have a formula to calculate this kind of numbers in a constant time but is there something like that for fibonacci numbers?
And after a very very little searching on stackexchange we can find a matrix identity for it! 

https://math.stackexchange.com/questions/1124590/need-help-understanding-fibonacci-fast-doubling-proof

F(2k)=F(k)[2F(k+1)−F(k)]
F(2k +1) = F(k+1)2+F(k)2

Where the fist one its for even numbers and the last for odd, so we need to rembember that any positive integer n, it is the same as either 2m (even) or 2m+1 (odd), where m=n2/2
The we simply compute it! 
So i found a very good recursive implementation in: 

https://www.nayuki.io/page/fast-fibonacci-algorithms

But it is a recursive implementation so at some point it will give us a Maximum depth exceeded error, and for large numbers this algorithm will have efficiency problems, so, we will implement the same in a fully iterative way and in the code I will explain some of the optimizations I made to that code. 

def final_fibo(n: int):

    """Calculate the NTH fibo using iterative method and doing shift optimizations!"""
    # Define the base case!
    a, b = 0, 1
    # Now we need to calculate the halving of n! In the recursive way you have the last value becouse you dindt stop until we got a 0 but heare we need to obtain first the halving value then iterate it! 
    halving = []
    while n:
        #   First optimization in python you have 2 different ways to append to a list the common one ".append" and the less common "extend"
        #   Extend optimizes the addition of new elements to the list when they are very large elements such as the calculated fibbonacci numbers.
        #   See more: https://stackoverflow.com/questions/252703/what-is-the-difference-between-pythons-list-methods-append-and-extend
        halving.extend([n])
        #   In python are two ways to round floor division: the floor division and the right shift
        #   Using the bitwise right shift was a common way of improving the performance of some arithmetic divisions.
        #   That improve its becouse the >> operator is only 1 instruccion on assembler
        #   About shift operation https://realpython.com/python-bitwise-operators/
        n >>= 1
    # Now we have all the halving complete so we need to calculate the identities!
    while(halving):
        c = a * ((b*2) - a)
        d = a * a + b * b
        # Now you can tell me n % 2 its slower than n&1! but in python and in c this operation its optimized a produces the same result in assamby or middle code 
        # so for a better understanding of the code i decide to use %2 and we eliminate the need to use the comparator == changing the order of the operations =) !
        if halving.pop() % 2:
            a, b = d, c + d
        else:
            a, b = c, d
    return a

Some test to the api!

### NFO:main: TIMING: Wall:    0.9ms | CPU:    0.9ms | app.main.final

#### INFO:     127.0.0.1:54054 - "GET /final?number=10 HTTP/1.1" 200 OK

### INFO:main: TIMING: Wall:    0.6ms | CPU:    0.6ms | app.main.calculate_Fib

#### INFO:     127.0.0.1:54060 - "GET /optimal?number=10 HTTP/1.1" 200 OK

### INFO:main: TIMING: Wall: 46921.7ms | CPU: 46886.9ms | app.main.calculate_Fib

#### INFO:     127.0.0.1:54100 - "GET /optimal?number=10000000 HTTP/1.1" 200 OK

### INFO:main: TIMING: Wall: 46100.0ms | CPU: 46084.9ms | app.main.final

#### INFO:     127.0.0.1:54108 - "GET /final?number=10000000 HTTP/1.1" 200 OK

As you can see in the tests the recursive algorithm is faster when the numbers are very small but that changes when the number goes over 6 digits! This is because in the final algorithm we have two cycles! And in the recursive one we only do it once. But once the price of recursion starts to show, our final algorithm gains a big advantage.

Then if we got a database we can for sure use memoization! To optimize the final algorithm, and then we can implement the Karatzuba algorithm in the multiplications! 

## How to run this :) 

```
virtualenv env
source /env/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

## Endpoints

Then the last we have 3 endpoints

## /easy   
    """Calculate the NTH fibo using the count method"""
## /optimal
    """Calculate the NTH fibo using doubling method (recursive)"""
## /final
    """Calculate the NTH fibo using doubling method (iterative and optimized)"""

All these endpoints receive a parameter called number which is the index of the fibonacci number, for example:

https://fibo-api-osmar.herokuapp.com/final?number=10
https://fibo-api-osmar.herokuapp.com/optimal?number=10
https://fibo-api-osmar.herokuapp.com/easy?number=10

## You can try it in but please dont exced of the 10,000,000 number :)
https://fibo-api-osmar.herokuapp.com/easy?number=10