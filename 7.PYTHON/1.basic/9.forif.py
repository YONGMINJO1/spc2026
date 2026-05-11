numbers = [1,2,3,4,5]

for num in numbers:
    if num % 2 == 0:
        print(f"숫자 {num}은 짝수 입니다.")
    else:
        print(f"숫자 {num}은 홀수 입니다.")

import time
n = 100
count = 0
# 코드의 효율성 .... 시간복잡도/공간복잡도
start_time = time.time() # 현재 시간
for i in range(n):
    for j in range(n):
        for k in range(n):
            for l in range(n):
                count += 1

end_time = time.time()
exec_time = end_time - start_time

print("합산: ", count)
print(f"총 소요시간은: {exec_time:.1f} 초가 소요되었습니다.")