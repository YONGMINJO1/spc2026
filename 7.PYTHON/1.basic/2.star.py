print("*")
print("**")
print("***")
print("****")
print("*****")
print("******")

print("=" * 20)
print("=     성적표       =")
print("=" * 20)


print("\n - 1 - ")
for i in range(1, 6):  # 1부터 출발해서 6을 포함하지 않는것
    print("*" * i)

print("\n - 2 - ")
n = 5
for i in range(1, 6):
    print(" " * (n - i), end="")  # 공백을 찍는 부분
    print("*" * i)  # *을 찍는 부분
    # print(" " *(n-i) + "*" * i)

print("\n - 3 - ")

for i in range(1, 6):
    print(
        " " * (5 - i) + "*" * (2 * i - 1)
    )  # 공백부분 +  *부분 (1,3,5,7,9) 어떻게 만들지
