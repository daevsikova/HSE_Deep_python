def fibonacci(n):
    output = [0] if n == 1 else [0, 1]
    for i in range(2, n):
        output.append(output[i - 1] + output[i - 2])
    return output
