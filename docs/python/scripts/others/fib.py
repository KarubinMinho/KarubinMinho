'''
def fib(N):
    """
    :type N: int
    :rtype: int
    """
    if N <= 1:
        return N
    else:
        return fib(N-1) + fib(N-2)

for i in range(20):
    print(fib(i))
'''


def fib(N):
    if N <= 1:
        return N
    return mem(N)

def mem(N):
    cache = {0: 0, 1: 1}
    for i in range(2, N+1):
        cache[i] = cache[i-1] + cache[i-2]
    print(cache)
    return cache[N]

print(fib(20))
# 做得不错，不过，这样子的话，运算效率相对差一些
