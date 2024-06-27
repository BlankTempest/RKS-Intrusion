def de_bruijn(n):
    a = [0] * (2 * n)
    sequence = []

    def db(t, p):
        if t > n:
            if n % p == 0:
                for j in range(1, p + 1):
                    sequence.append(a[j])
        else:
            a[t] = a[t - p]
            db(t + 1, p)
            for j in range(a[t - p] + 1, 2):
                a[t] = j
                db(t + 1, t)

    db(1, 1)
    return sequence

def print_de_bruijn(n):
    sequence = de_bruijn(n)
    de_bruijn_str = ''.join(str(i) for i in sequence)
    print(de_bruijn_str)

n = int(input("Enter 2^n:\n"))
print_de_bruijn(n)