import qrcode
from PIL import Image
import os
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------
# CONFIGURACIÓN
# -----------------------------------------

URL_PLAY_STORE = os.getenv("URL_PLAY_STORE")

LOGO_PATH = os.getenv("LOGO_PATH")
name_logo = os.path.split(LOGO_PATH)[len(os.path.split(LOGO_PATH)) - 1]
print(name_logo)
OUTPUT_PATH = f"./output/{os.path.splitext(name_logo)[0]}.png"

# Tamaño del QR
BOX_SIZE = 20

# -----------------------------------------
# CREAR QR
# -----------------------------------------

qr = qrcode.QRCode(
    version=None,
    error_correction=qrcode.constants.ERROR_CORRECT_H,
    box_size=BOX_SIZE,
    border=4
)

qr.add_data(URL_PLAY_STORE)
qr.make(fit=True)

qr_image = qr.make_image(
    fill_color="#0F172A",
    back_color="white"
).convert("RGB")

# -----------------------------------------
# CARGAR LOGO
# -----------------------------------------

logo = Image.open(LOGO_PATH).convert("RGBA")

# El logo ocupará aproximadamente el 20 %
# del ancho del QR.
qr_width, qr_height = qr_image.size

logo_size = int(qr_width * 0.20)

logo.thumbnail((logo_size, logo_size), Image.Resampling.LANCZOS)

# -----------------------------------------
# CREAR FONDO BLANCO PARA EL LOGO
# -----------------------------------------

padding = 20

logo_background = Image.new(
    "RGB",
    (
        logo.width + padding * 2,
        logo.height + padding * 2
    ),
    "white"
)

# -----------------------------------------
# PEGAR LOGO SOBRE EL FONDO
# -----------------------------------------

logo_background_rgba = logo_background.convert("RGBA")

logo_background_rgba.alpha_composite(
    logo,
    (
        padding,
        padding
    )
)

logo_background = logo_background_rgba.convert("RGB")

# -----------------------------------------
# CENTRAR LOGO
# -----------------------------------------

position = (
    (qr_width - logo_background.width) // 2,
    (qr_height - logo_background.height) // 2
)

qr_image.paste(
    logo_background,
    position
)

# -----------------------------------------
# GUARDAR
# -----------------------------------------

qr_image.save(
    OUTPUT_PATH,
    "PNG",
    dpi=(300, 300)
)

print(f"QR generado correctamente: {OUTPUT_PATH}")
