def draw_square(size):
    for i in range(size):
        print("🧱"*size)


draw a triangle like this *size = 5
def draw_triangle(size):
    for i in range(size):
        print(" "*(size-i-1) + "*"*(i+1))   