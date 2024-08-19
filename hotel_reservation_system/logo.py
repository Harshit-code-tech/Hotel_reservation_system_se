import os
import random
from PIL import Image, ImageDraw, ImageFont


def generate_random_color():
    return (random.randint(100, 255), random.randint(100, 255), random.randint(100, 255))


def add_gradient(draw, width, height, color1, color2):
    for i in range(height):
        color = tuple(
            int(color1[j] + (float(i) / height) * (color2[j] - color1[j])) for j in range(3)
        )
        draw.line([(0, i), (width, i)], fill=color)


def generate_random_hotel_structure(draw):
    building_color = (random.randint(200, 240), random.randint(150, 200), random.randint(100, 150))
    building_width = random.randint(400, 624)
    building_height = random.randint(300, 424)
    x_start = random.randint(200, 400)
    y_start = 824 - building_height

    draw.rectangle([x_start, y_start, x_start + building_width, 824], fill=building_color)

    # Draw windows
    for x in range(x_start + 40, x_start + building_width - 40, 80):
        for y in range(y_start + 40, 824 - 80, 80):
            draw.rectangle([x, y, x + 60, y + 60], fill="white")  # Windows
            draw.line([x, y, x + 60, y + 60], fill="gray", width=2)
            draw.line([x + 60, y, x, y + 60], fill="gray", width=2)

    # Draw hotel entrance
    entrance_width = random.randint(100, 224)
    entrance_height = random.randint(100, 124)
    draw.rectangle([x_start + (building_width - entrance_width) // 2, 824 - entrance_height, x_start + (building_width + entrance_width) // 2, 824], fill=(169, 169, 169))
    draw.rectangle([x_start + (building_width - entrance_width) // 2 + 40, 824 - entrance_height + 50, x_start + (building_width + entrance_width) // 2 - 40, 824], fill="brown")

    # Draw roof
    draw.polygon([(x_start, y_start), (x_start + building_width, y_start), (x_start + building_width // 2, y_start - 100)], fill="darkred")


def generate_hotel_image(save_path):
    image = Image.new("RGB", (1024, 1024), generate_random_color())
    draw = ImageDraw.Draw(image)

    # Draw sky with gradient
    add_gradient(draw, 1024, 400, (135, 206, 235), (70, 130, 180))

    # Draw hotel with varied structure
    generate_random_hotel_structure(draw)

    image.save(save_path)


def generate_random_mountain_structure(draw):
    base_height = random.randint(400, 500)
    peak_height = random.randint(200, 300)
    peak_offset = random.randint(-100, 100)

    # Draw mountains with random structure
    draw.polygon([(200 + peak_offset, 824), (512, base_height), (824 + peak_offset, 824)], fill=(34, 139, 34))  # Main mountain
    draw.polygon([(312 + peak_offset, 824), (512, base_height + 100), (712 + peak_offset, 824)], fill=(50, 205, 50))  # Second mountain
    draw.polygon([(412 + peak_offset, 824), (512, base_height + 200), (612 + peak_offset, 824)], fill=(60, 179, 113))  # Third mountain

    # Draw snowcaps
    draw.polygon([(462 + peak_offset, base_height - 50), (512, base_height - 100), (562 + peak_offset, base_height - 50)], fill="white")
    draw.polygon([(412 + peak_offset, base_height + 50), (512, base_height), (612 + peak_offset, base_height + 50)], fill="white")



def generate_mountain_image(save_path):
    image = Image.new("RGB", (1024, 1024), (135, 206, 235))  # Sky color
    draw = ImageDraw.Draw(image)

    # Draw mountains with varied structure
    generate_random_mountain_structure(draw)

    # Add some trees with random positions
    tree_color = (0, 100, 0)
    for i in range(random.randint(5, 10)):
        x = random.randint(200, 824)
        draw.polygon([(x, 824), (x - 20, 784), (x + 20, 784)], fill=tree_color)
        draw.polygon([(x, 784), (x - 15, 754), (x + 15, 754)], fill=tree_color)
        draw.polygon([(x, 754), (x - 10, 734), (x + 10, 734)], fill=tree_color)

    image.save(save_path)


def generate_beach_image(save_path):
    image = Image.new("RGB", (1024, 1024), (135, 206, 235))  # Sky color
    draw = ImageDraw.Draw(image)

    # Draw sea with gradient
    add_gradient(draw, 1024, 400, (0, 191, 255), (25, 25, 112))

    # Draw sand
    sand_color = (237, 201, 175)
    draw.rectangle([0, 624, 1024, 1024], fill=sand_color)
    for i in range(50):
        x = random.randint(0, 1024)
        y = random.randint(624, 1024)
        radius = random.randint(5, 15)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(210, 180, 140))

    # Draw sun
    draw.ellipse([random.randint(700, 900), random.randint(50, 150), random.randint(850, 1024), random.randint(200, 300)], fill=(255, 223, 0))

    # Draw waves with varied heights
    for i in range(random.randint(3, 7)):
        wave_height = random.randint(30, 60)
        draw.arc([0, 524 + i * wave_height, 1024, 624 + i * wave_height], 0, 180, fill="white", width=3)

    image.save(save_path)


def create_logo_folders_with_images(base_dir, num_logos):
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)

    for i in range(1, num_logos + 1):
        logo_dir = os.path.join(base_dir, f'logo {i}')
        os.makedirs(logo_dir, exist_ok=True)

        generate_hotel_image(os.path.join(logo_dir, 'hotel_image.png'))
        generate_beach_image(os.path.join(logo_dir, 'beach_image.png'))
        generate_mountain_image(os.path.join(logo_dir, 'mountain_image.png'))


if __name__ == "__main__":
    base_dir = "logos"
    num_logos = 10

    create_logo_folders_with_images(base_dir, num_logos)
    print(f"Created {num_logos} logo folders with unique images in the '{base_dir}' directory.")
