# List comprehension: builds the full list now
squares_list = [x ** 2 for x in range(1_000_000)]

# Generator expression: computes values as they are requested
squares_gen = (x ** 2 for x in range(1_000_000))

squares_before_break = []
for s in squares_gen:
    if s > 100:
        break
    squares_before_break.append(s)

print(squares_before_break)  # [0, 1, 4, 9, 16, 25, 36, 49, 64, 81, 100]