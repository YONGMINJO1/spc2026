# 1. 작은 파일 읽기
with open("file.text","r",encoding="utf-8") as file:
    data = file.read()
    print("파일 내용은 : ", data)

# 2. 레거시 파일 읽기
# file = open("file.text","r",encoding="utf-8")
# data = file.read()
# file.close()
# print(data)

# 3. 큰 파일 읽기
with open("file.text","r",encoding="utf-8") as file:
    lines = file.readline()

    for line in lines:
        print("파일 내용은 : ", line)