# for stickers
from PIL import Image

def add_black_outline(path, output_path, border_size=10):
    img = Image.open(path)
    outlined_img = Image.new('RGB', img.size, (0, 0, 0))
    outlined_img.paste(img, (0, 0))
    for y in range(border_size):
        for x in range(img.size[0]):
            outlined_img.putpixel((x, y), (0, 0, 0))
            outlined_img.putpixel((x, img.size[1]-1-y), (0, 0, 0))
            outlined_img.putpixel((y, x), (0, 0, 0))
            outlined_img.putpixel((img.size[0] - 1 - y, x), (0, 0, 0))
            pass

    outlined_img.save(output_path)
    outlined_img.close()
    img.close()

for p in ['green.png', 'red.png', 'blue.png', 'white.png', 'yellow.png', 'orange.png']:
    out_path='textures/'+p[0].upper()+'.png'
    p='textures/'+p
    add_black_outline(p, out_path, border_size=80)