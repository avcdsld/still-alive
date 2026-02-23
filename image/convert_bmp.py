#!/usr/bin/env python3
"""Convert 24-bit BMP to e-paper binary format (black + red buffers)"""

import struct

def convert_bmp(input_file, output_black, output_red):
    with open(input_file, 'rb') as f:
        # Read BMP header
        header = f.read(54)

        # Parse header
        width = struct.unpack('<I', header[18:22])[0]
        height = struct.unpack('<I', header[22:26])[0]
        bpp = struct.unpack('<H', header[28:30])[0]

        print(f"Image: {width}x{height}, {bpp}bpp")

        if bpp != 24:
            print(f"Error: Expected 24bpp, got {bpp}bpp")
            return

        # Calculate row padding (BMP rows are 4-byte aligned)
        row_size = ((width * 3 + 3) // 4) * 4

        # Prepare output buffers
        black_buffer = bytearray(height * width // 8)
        red_buffer = bytearray(height * width // 8)

        # Read pixel data (BMP is bottom-up)
        for y in range(height - 1, -1, -1):
            row_data = f.read(row_size)
            for x in range(width):
                # BGR format
                b = row_data[x * 3]
                g = row_data[x * 3 + 1]
                r = row_data[x * 3 + 2]

                # Determine color
                # White: r>200, g>200, b>200
                # Red: r>200, g<100, b<100
                # Black: everything else

                byte_idx = y * (width // 8) + x // 8
                bit_idx = 7 - (x % 8)

                if r > 200 and g > 200 and b > 200:
                    # White: black=1, red=0
                    black_buffer[byte_idx] |= (1 << bit_idx)
                elif r > 200 and g < 100 and b < 100:
                    # Red: black=1, red=1
                    black_buffer[byte_idx] |= (1 << bit_idx)
                    red_buffer[byte_idx] |= (1 << bit_idx)
                else:
                    # Black: black=0, red=0
                    pass

        # Write output files
        with open(output_black, 'wb') as f:
            f.write(black_buffer)
        with open(output_red, 'wb') as f:
            f.write(red_buffer)

        print(f"Created: {output_black} ({len(black_buffer)} bytes)")
        print(f"Created: {output_red} ({len(red_buffer)} bytes)")

if __name__ == '__main__':
    convert_bmp('message.bmp', 'image_black.bin', 'image_red.bin')
