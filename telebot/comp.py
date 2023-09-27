x = int(input())

for i in range(x):
    y = int(input())
    num = list(map(int, input().split()))
    stack = []
    store = {}
    ans = y
    for j in range(y):
        store[num[y - 1 - j]] = store.get(num[y - j - 1], 0) + 1
        if store[num[y - j - 1]] > 1:
            break
        ans -= 1
    print(ans)
