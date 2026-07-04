def square(x):
    return x+x

operation = square
print(operation(5))

def apply_to_list(func, items):
    return [func(item,item+1) for item in items]

scores = [0.8, 0.3, 0.95, 0.4]
normalized = apply_to_list(lambda x,y: round(x*10*y), scores)
print(normalized)