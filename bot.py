def get_font(size: int):
    """Charge une police lisible. Mets un fichier .ttf à côté de bot.py pour un meilleur rendu."""
    for path in (Path(__file__).parent / "police.ttf", "DejaVuSans-Bold.ttf"):
        try:
            return ImageFont.truetype(str(path), size)
        except OSError:
            continue
    try:
        return ImageFont.load_default(size=size)  # Pillow 10.1 ou plus récent
    except TypeError:
        return ImageFont.load_default()


def build_card_image(name: str, avatar_bytes: bytes) -> io.BytesIO:
    W, H = 1000, 560
    img = Image.new("RGB", (W, H), (14, 14, 24))
    draw = ImageDraw.Draw(img)

    # Cadre
    draw.rectangle((10, 10, W - 10, H - 10), outline=(70, 70, 95), width=2)

    # Avatar rond
    avatar = Image.open(io.BytesIO(avatar_bytes)).convert("RGBA").resize((150, 150))
    mask = Image.new("L", (150, 150), 0)
    ImageDraw.Draw(mask).ellipse((0, 0, 150, 150), fill=255)
    img.paste(avatar, (50, 50), mask)

    # Titre et pseudo
    draw.text((230, 70), name[:20], fill=(255, 255, 255), font=get_font(46))
    draw.text((230, 130), "STATUT", fill=(150, 150, 175), font=get_font(24))

    # Trois cartes : classement, messages, vocal
    cards = [
        ("CLASSEMENT", [("Messages", "#--"), ("Vocal", "#--"), ("XP", "#--")]),
        ("MESSAGES", [("1j", "0"), ("7j", "0"), ("30j", "0")]),
        ("ACTIVITÉ VOCALE", [("1j", "0 h"), ("7j", "0 h"), ("30j", "0 h")]),
    ]
    x = 40
    for title, rows in cards:
        draw.rounded_rectangle((x, 270, x + 290, 520), radius=12, fill=(24, 24, 40), outline=(70, 70, 95), width=2)
        draw.text((x + 18, 285), title, fill=(200, 200, 225), font=get_font(22))
        y = 335
        for label, value in rows:
            draw.text((x + 18, y), label, fill=(150, 150, 175), font=get_font(24))
            draw.text((x + 150, y), value, fill=(255, 255, 255), font=get_font(28))
            y += 55
        x += 315

    buffer = io.BytesIO()
    img.save(buffer, "PNG")
    buffer.seek(0)
    return buffer
