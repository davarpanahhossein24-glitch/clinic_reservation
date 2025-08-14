# def hello(name):
#
#     def hello_amir():
#         print(f'Hello {name}')
#
#     return hello_amir
#
# new=hello('Amir')
# new()


def decorator(func):
    def wrapper():
        print("Before calling the function.")
        func()
        print("After calling the function.")

    return wrapper

def decorator2():
    print("hi user.")


new=decorator(decorator2)
new()