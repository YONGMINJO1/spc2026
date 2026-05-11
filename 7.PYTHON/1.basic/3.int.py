# 숫자를 할당하면? int 타입
x = 5
y = 3

# 4칙 연산
print(x + y)
print(x - y)
print(x * y)
print(x / y)

# 나머지
print(x % y) # x를 y로 나눈 나머지 값 : 5 나누기 3은 1 나머지2

# 제곱 (^ 쓰지 않는다.)
print(x ** y)

# 진법 변환
print(bin(x)) # 2진수 0b
print(oct(x)) # 8진수 0o
print(hex(x)) # 16진수 0x

x = - 10
print(x)
print(abs(x))

y = 4.5
print(y)
print(int(y))

z = "100"
print(z) # 문자열 100
print(int(z)) # 슷지 100

# 비트 연산자 (AND , OR, XOR, NOT)
x = 5
y = 3
print(x & y) # 5 = 101 / 3 = 011,  5 AND 3 = 101 AND 011 = 001
print(x | y) # 5 = 101 / 3 = 011,  5 OR 3 = 101 OR 011 = 111
print(x ^ y) # XOR = 110
print(~x) # NOT x 00000101 = 11111010 <- 첫째자리가 부호

print(x << 1) # 왼쪽으로 한자리 이동 0000 0101 << 1 = 00001010
print(x >> 1) # 오른쪽으로 한자리 이동 0000 0101 >> 1 = 00000101