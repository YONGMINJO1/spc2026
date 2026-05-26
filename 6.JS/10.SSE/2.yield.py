def test():
    print('A') # 이 함수가 수행할 다양한 일
    yield 1    # 여기에서 일단 멈춤 (return 1)

    print('B') # 이 함수가 수행할 그 다음 다양한 일
    yield 2    # 여기에서 일단 멈춤 (return 2)

    print('C') # 이 함수가 수행할 그 다음 다양한 일
    yield 3    # 여기에서 일단 멈춤 (return 3)

x = test() # generator 라는 것이 만들어짐 - 동적으로 바뀌는 데이터를 전달하는 객체

# print(x)

# 다음 것을 알아서 만들어서 보내줌
print(next(x))
print(next(x))
print(next(x))

try:
    while True:
        print(next(x))

except StopAsyncIteration:
    print('모든 데이터 사용 완료')