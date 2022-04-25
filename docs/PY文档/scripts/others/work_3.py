import random

#  1.
lst = [1, 4, 9, 16, 2, 5, 10, 15]

# new_l = []  
# for i in range(len(lst)-1):
#    new_l.append(lst[i] + lst[i+1])
new_l = [lst[i] + lst[i+1] for i in range(len(lst)-1)]

# 这里，这个新列表，一言难尽
print(new_l)

# 2.

random_list = []
for i in range(20):
    random_list.append(random.randint(0, 20))

# compare_list = []
# for i in range(20):
#     compare_list.append((i, random_list.count(i)))
compare_set = {(i, random_list.count(i)) for i in range(20)} #这里使用count，现在数据量小还没问题，数据量大的话，效率会很差

for k, v in sorted(compare_set, key=lambda x: x[1], reverse=True)[:3]:
    print("value: {:<5} count_num: {}".format(k, v))

# 3.
# for i in range(26):
#    print(chr(97 + i))
letters_list = [chr(97+i) for i in range(26)]
for i in range(100):
    print("{:0>6}.{}".format(i, ''.join(random.choices(letters_list, k=10))))


# 4.
s = 'abcdefghijklmnopqrstuvwxyz'
# for i in range(100):
#     print(''.join(random.choices(s, k=2)))
s_list = [''.join(random.choices(s, k=2)) for i in range(100)]
# for i in s_list:
#    print(s_list.count(i))
s2_set = {(i, s_list.count(i)) for i in s_list}
for k, v in sorted(s2_set, key=lambda x: x[1], reverse=True):
    print("str: {} counts: {}".format(k, v))
