def fib(n):
    a= 0
    b = 1 
    for _ in range(n):
        siguiente = a + b  # calculamos el siguiente término
        a = b              # el nuevo Fiboinaci pasa a ser el anterior 
        b = siguiente      # el nuevo Fibonaci+1
    return a

# improimir un eejemplo
print(fib(10))  # 55