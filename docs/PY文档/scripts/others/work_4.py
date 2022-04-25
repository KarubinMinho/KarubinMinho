def func(n):
    length = len(' '.join([str(x) for x in range(1, n+1)]))
    # 1.
    for x in range(1, n+1):
        l = []
        for y in range(x, 0, -1):
            l.append(str(y))
        out_s = ' '.join(l)
        print("{:>{width}}".format(out_s, width=length))
        print()
    # 2.
    for x in range(n, 0, -1):
        l = []
        for y in range(x, 0, -1):
            l.append(str(y))
        out_s = ' '.join(l)
        print("{:>{width}}".format(out_s, width=length))
        print()

func(12)


# 这里两行之间，可以省略的空行，不过，无伤大雅，整体做得不错，点赞
