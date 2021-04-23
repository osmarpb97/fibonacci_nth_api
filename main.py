import logging
from fastapi import FastAPI, HTTPException
from fastapi_utils.timing import add_timing_middleware, record_timing

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

add_timing_middleware(app, record=logger.info, prefix="app", exclude="untimed")


@app.get("/easy")
def calculate_FibEasy(number: int) -> int:
    if(number < 0):
        raise HTTPException(
            status_code=500, detail="The number must be an positive integer")
    return fibo_easy(number)


@app.get("/optimal")
def calculate_Fib(number: int) -> int:
    if(number < 0):
        raise HTTPException(
            status_code=500, detail="The number must be an positive integer")
    return fibo(number)[0]


@app.get("/final")
def final(number: int) -> int:
    if(number < 0):
        raise HTTPException(
            status_code=500, detail="The number must be an positive integer")
    return final_fibo(number)


def final_fibo(n: int):
    """Calculate the NTH fibo using iterative method and doing shift optimizations!"""
    # Define the base case!
    a, b = 0, 1
    # Now we need to calculate the halving of n!
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
        c = a * (b *2 - a)
        d = a * a + b * b
        # Now you can tell me n % 2 its slower than n&1! but in python and in c this operation its optimized a produces the same result in assamby or middle code 
        # so for a better understanding of the code i decide to use %2 and we eliminate the need to use the comparator == changing the order of the operations =) !
        if halving.pop() % 2:
            a, b = d, c + d
        else:
            a, b = c, d
    return a


def fibo(n: int):
    """Calculate the NTH fibo using doubling method"""
    if n == 0:
        return (0, 1)
    else:
        a, b = fibo(n // 2)
        c = a * (b * 2 - a)
        d = a * a + b * b
        if n % 2 == 0:
            return (c, d)
        else:
            return (d, c + d)


def fibo_easy(n: int):
    """Calculate the NTH fibo using the count method"""
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a+b
    return a
