print('Hello, Python')
print('Hello', 'Python')
print('Hello, ' +  'Python')
print("Hello, " +  'Python')
print('"Hello, "' +  "'Python'")
print('"Hello, "' +  "'Python'" + "!!")
num = 5
name = "홍길동"
print("hello, {}".format(name))
print("hello, {}.My lucky number is {}".format(name, num))
print("hello, {0}.My lucky number is {1}".format(name, num))
print("hello, {1}.My lucky number is {0}".format(name, num))
print("hello, %s" % name)
print("hello, %s" % name, end="")
print(' 홍길동', end="" )
print(' 홍길동', end="\n" )

multline = """
여기는 멀티라인으로 
긴 주석을 넣을 수 있음
사실은 주석은 아니고 여러줄의 문자열임
"""

print(multline)
