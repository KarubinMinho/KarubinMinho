# for循环嵌套
for x in range(1, 10):
    for y in range(1, x+1):
        print("{} * {} = {}".format(y, x, x*y), end='\t')
    print()

print('='*90)
# 列表推导式嵌套
# 列表推导式的结果可以是另一个列表推导式
print('\n'.join(['\t'.join(["{} * {} = {}".format(y, x, x*y) for y in range(1, x+1)]) for x in range(1, 10)]))


# 这里的做得不错，点赞
