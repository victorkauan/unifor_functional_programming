from PIL import Image

# Constants
IMAGE_PATH = lambda: r"C:\Users\Dev M7\PycharmProjects\functional_programming\q3\image.jpg"

# Functions
# - Messages
question_title = lambda: print("QUESTION 03 BY VICTOR KAUAN LIMA DE OLIVEIRA")
default_rgb_value_message = lambda: print("Obs.: Press enter to use the default value (0)")
rgb_values_message = lambda: print("Enter the RGB values to brighten the image: ")
show_images_success = lambda: print("[SUCCESS] The original and modified images were opened successfully")

# - Utilities
get_rgb_value = lambda value: max(0, min(value, 255))
zero_if_is_empty = lambda value: 0 if value == "" else value
get_modified_image_path = lambda image_path: image_path.replace(".jpg", "_modified.jpg")
sum_rgb_values = lambda rgb_values: lambda rgb: [
    get_rgb_value(rgb_values[index] + rgb[index])
    for index in range(len(rgb_values))
]

# - Image
read_image = lambda image_path: Image.open(fp=image_path)
get_image_info = lambda image: [[image.getpixel((x, y)) for y in range(image.height)] for x in range(image.width)]
get_modified_image_info = lambda function, image: [
    [function(pixel) for pixel in line]
    for line in get_image_info(image)
]
put_image_pixels = lambda image, image_info: [
    [image.putpixel((x, y), tuple(pixel)) for y, pixel in enumerate(line)]
    for x, line in enumerate(image_info)
]
save_image = lambda image, image_path: image.save(fp=image_path)
show_image = lambda image: image.show()

enter_image_path = lambda: input("Enter the image path, if you want to use the default image, just press enter: ")
get_r_value = lambda: int(zero_if_is_empty(input("R (Red): ")))
get_g_value = lambda: int(zero_if_is_empty(input("G (Green): ")))
get_b_value = lambda: int(zero_if_is_empty(input("B (Blue): ")))

get_rgb_values = lambda: (get_r_value(), get_g_value(), get_b_value())

# - Execution
transform_image = lambda image_path, image, function: (
    put_image_pixels(image, get_modified_image_info(function, image)),
    save_image(image, get_modified_image_path(image_path)),
    read_image(image_path).show(),
    show_image(image),
)

if __name__ == "__main__":
    question_title() or print()
    user_image_path = enter_image_path() or IMAGE_PATH()
    print() or transform_image(
        user_image_path,
        read_image(user_image_path),
        sum_rgb_values(default_rgb_value_message() or get_rgb_values())
    )
    print() or show_images_success()
