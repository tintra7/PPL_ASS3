class IntegerType:
    pass

class BooleanType:
    pass

class FloatType:
    pass
 
a = None

def foo(ls, i):
    if i == (len(ls) - 1):
        return True
    if ls[i] < 0:
        return False
    return foo(ls, i + 1)

print(foo([1,-2,3],0))