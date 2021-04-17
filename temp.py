a = 0
def princ():
    global a
    a += 1
    a += 3
    print(a)
    global b
    b = 5

if __name__ == '__main__':
    princ()
    a += 10
    print(a)
    print(b)