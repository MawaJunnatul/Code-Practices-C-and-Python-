my_array = list(map(int, input("Enter comma separated values").split(",")))
n = len(my_array)
ans = []
maxi = 0
for i in reversed(range(n)):
    if my_array[i] >= maxi:
        ans.append(my_array[i])
    maxi = max(my_array[i], maxi)
ans.reverse()
print(ans)

