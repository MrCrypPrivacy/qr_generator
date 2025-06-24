from PIL import Image, ImageDraw
import qrcode

def generate_qr_code(data, qr_color="#000000", bg_color="#FFFFFF", logo_path=None, size=300, style="square"):
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_H,
        box_size=10,
        border=1,
    )
    qr.add_data(data)
    qr.make(fit=True)

    matrix = qr.get_matrix()
    matrix_size = len(matrix) + qr.border * 2

    box_size = size // matrix_size
    pixel_size = box_size * matrix_size

    img = Image.new("RGB", (pixel_size, pixel_size), bg_color)
    draw = ImageDraw.Draw(img)

    for y, row in enumerate(matrix):
        for x, val in enumerate(row):
            if val:
                x0 = (x + qr.border) * box_size
                y0 = (y + qr.border) * box_size
                x1 = x0 + box_size
                y1 = y0 + box_size

                if style == "dots":
                    draw.ellipse([x0, y0, x1, y1], fill=qr_color)
                elif style == "rounded":
                    radius = box_size // 3
                    draw.rounded_rectangle([x0, y0, x1, y1], radius=radius, fill=qr_color)
                else:
                    draw.rectangle([x0, y0, x1, y1], fill=qr_color)

    if logo_path:
        try:
            logo = Image.open(logo_path).convert("RGBA")
            max_logo_size = pixel_size // 4
            logo.thumbnail((max_logo_size, max_logo_size), Image.LANCZOS)

            pos = ((img.size[0] - logo.size[0]) // 2, (img.size[1] - logo.size[1]) // 2)
            img.paste(logo, pos, mask=logo)
        except Exception as e:
            print("ERROR insertando logo:", e)

    return img


if __name__ == "__main__":
    img = generate_qr_code(
        "https://mrcryp.privacy",
        qr_color="#00FF00",
        bg_color="#222222",
        style="rounded",
        size=300
    )
    img.show()
