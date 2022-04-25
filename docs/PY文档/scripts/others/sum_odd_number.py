# range I
odd_sum1 = 0
for i in range(100):
    if i & 1:  # or  if i % 2: odd_sum1 += i
        odd_sum1 += i
print(odd_sum1)

# range II
odd_sum = 0
for i in range(1, 100, 2):
    odd_sum += i
print(odd_sum)

# range III
l = []
for i in range(1, 100, 2):
    l.append(i)
print(sum(l))


# 做得不错，运用多种方法解题，点赞
