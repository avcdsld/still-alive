from epaper7in5b import EPD_7in5_B

epd = EPD_7in5_B()

def display_image(black_file, red_file):
    # Read directly into existing buffers (no extra memory allocation)
    with open(black_file, 'rb') as f:
        f.readinto(epd.buffer_black)

    with open(red_file, 'rb') as f:
        f.readinto(epd.buffer_red)

    epd.display()
    epd.sleep()

display_image('image_black.bin', 'image_red.bin')
