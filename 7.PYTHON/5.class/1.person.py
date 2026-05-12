class Person:
    def __init__(self,name,age):
        self.name = name
        self.age = age

    def great(self):
        print(f"안녕하세요, 저는 {self.name}입니다.")

    def study(self, subject):
        print(f"{self.name}는 {subject}를 공부하고 있습니다.")

person1 = Person("Alice",21)
person2 = Person("Boo",21)

person1.great()
person2.great()

person1.study("JAVA")
person2.study("PYTHON")