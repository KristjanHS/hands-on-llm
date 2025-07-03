def calculate_volume(height: int, area: int) -> int:
    volume = height * area    # should be 150
    return volume

box_length = 5
box_width = 10
box_height = 3
rectangle_area = box_length * box_width
box_volume = calculate_volume(box_height, rectangle_area)
print(box_volume)