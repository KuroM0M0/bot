import io
import aiohttp
from PIL import Image, ImageDraw, ImageFont
import discord


async def fetch_avatar(user, size=128):
    url = str(user.display_avatar.with_size(size).url)
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as resp:
            if resp.status != 200:
                raise Exception(f"Fehler beim Laden des Avatars für {user.display_name}")
            data = await resp.read()
            avatar = Image.open(io.BytesIO(data))
            if getattr(avatar, "is_animated", False):
                avatar.seek(0)
            avatar = avatar.convert("RGBA")
            return avatar.resize((size, size))
    pass


def paste_avatar(base_img: Image.Image, avatar: Image.Image, pos: tuple):
    base_img.paste(avatar, pos, avatar)


def paste_circle_avatar(base_img, avatar, pos, size):
    avatar = avatar.resize((size, size))
    mask = Image.new("L", (size, size), 0)
    draw = ImageDraw.Draw(mask)
    draw.ellipse((0, 0, size, size), fill=255)
    base_img.paste(avatar, pos, mask)

def draw_text_centered(draw, text, center_x, y, font, color="white"):
    bbox = draw.textbbox((0, 0), text, font=font)
    w = bbox[2] - bbox[0]
    draw.text((center_x - w // 2 + 1, y + 1), text, fill="black", font=font)
    draw.text((center_x - w // 2, y), text, fill=color, font=font)


def calc_x_positions(count, avatar_size, total_width, margin=40):
    total_avatars_width = count * avatar_size + (count - 1) * margin
    start_x = (total_width - total_avatars_width) // 2
    return [start_x + i * (avatar_size + margin) for i in range(count)]

async def draw_descendant_tree(node, image, draw, x, y, avatar_size, level_height, font):
    """Rekursiv! Zeichnet alle Kinder eines Knotens und verbindet mit Linien."""
    width = image.width

    # Stoppbedingung: keine Kinder mehr
    if not node["children"]:
        avatar = await fetch_avatar(node["person"], avatar_size)
        paste_circle_avatar(image, avatar, (x - avatar_size // 2, y), avatar_size)
        draw_text_centered(draw, node["person"].display_name, x, y + avatar_size + 10, font)
        return x, x  # links/rechts

    # Positionen für Kinder berechnen
    num_children = len(node["children"])
    margin = 80
    total_width = num_children * avatar_size + (num_children - 1) * margin
    left_start = x - total_width // 2 + avatar_size // 2
    child_centers = []
    for idx, child_node in enumerate(node["children"]):
        cx = left_start + idx * (avatar_size + margin)
        min_cx, max_cx = await draw_descendant_tree(child_node, image, draw, cx, y + level_height, avatar_size, level_height, font)
        child_centers.append((cx, y + level_height))

    # Vertikale Linien von der Horizontalen zu jedem Kind
    for cx in child_xs:
        draw.line([(cx, mid_y - level_height // 2), (cx, mid_y)], fill="white", width=4)

    # Horizontale Linie auf Höhe der Kinder
    child_xs = [c[0] for c in child_centers]
    mid_y = y + level_height
    draw.line([(min(child_xs), mid_y), (max(child_xs), mid_y)], fill="white", width=4)

    # Vertikale Linie von „dir“ zur Horizontalen
    draw.line([(x, y + avatar_size), (x, mid_y - level_height // 2)], fill="white", width=4)

    # Avatar von „dir“ auf aktueller Ebene
    avatar = await fetch_avatar(node["person"], avatar_size)
    paste_circle_avatar(image, avatar, (x - avatar_size // 2, y), avatar_size)
    draw_text_centered(draw, node["person"].display_name, x, y + avatar_size + 10, font)

    return min(child_xs), max(child_xs)

async def generate_full_descendant_tree(root_node, width=1200, height=900, avatar_size=128, level_height=200):
    image = Image.new("RGBA", (width, height), "#D39242")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    # Start: mittig/oben
    x = width // 2
    y = 40
    await draw_descendant_tree(root_node, image, draw, x, y, avatar_size, level_height, font)
    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output


async def generate_ancestry_tree(user, parents, grandparents, width=1200, height=900, avatar_size=128):
    from PIL import ImageFont
    image = Image.new("RGBA", (width, height), "#D39242")
    draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.load_default()
    except:
        font = ImageFont.load_default()
    margin = 40
    v_spacing = 140

    # --- Positionen vorberechnen ---
    y_positions = [40, 40 + avatar_size + v_spacing, 40 + 2 * (avatar_size + v_spacing)]
    # Großeltern
    g_xs = calc_x_positions(len(grandparents), avatar_size, width, margin)
    g_centers = [(x + avatar_size // 2, y_positions[0] + avatar_size // 2) for x in g_xs]
    # Eltern
    p_xs = calc_x_positions(len(parents), avatar_size, width, margin)
    p_centers = [(x + avatar_size // 2, y_positions[1] + avatar_size // 2) for x in p_xs]
    # User
    user_x = width // 2 - avatar_size // 2
    user_center = (user_x + avatar_size // 2, y_positions[2] + avatar_size // 2)

    # --- Linien zuerst ---
    # --- Großeltern → Eltern ---
    mid_y_g2p = y_positions[0] + avatar_size + (v_spacing // 2)
    
    # Vertikale von jedem Großelternteil zur horizontalen Linie
    for gx, gy in g_centers:
        draw.line([(gx, gy + avatar_size // 2), (gx, mid_y_g2p)], fill="white", width=4)
    
    # Horizontale Linie, die alle Großeltern verbindet (über den Eltern)
    min_gx = min(g[0] for g in g_centers)
    max_gx = max(g[0] for g in g_centers)
    draw.line([(min_gx, mid_y_g2p), (max_gx, mid_y_g2p)], fill="white", width=4)
    
    # Vertikal von dieser Horizontalen zu jedem Elternteil
    for px, py in p_centers:
        draw.line([(px, mid_y_g2p), (px, py - avatar_size // 2)], fill="white", width=4)
    
    # --- Eltern → Du ---
    mid_y_p2u = y_positions[1] + avatar_size + (v_spacing // 2)
    
    # Vertikale von jedem Elternteil zur horizontalen Linie
    for px, py in p_centers:
        draw.line([(px, py + avatar_size // 2), (px, mid_y_p2u)], fill="white", width=4)
    
    # Horizontale Linie, die alle Eltern verbindet (über dir)
    min_px = min(p[0] for p in p_centers)
    max_px = max(p[0] for p in p_centers)
    draw.line([(min_px, mid_y_p2u), (max_px, mid_y_p2u)], fill="white", width=4)
    
    # Vertikale Linie von dieser Horizontalen zur Mitte deines Avatars
    draw.line([(user_center[0], mid_y_p2u), user_center], fill="white", width=4)

    # --- Avatare ---
    for x, gp in zip(g_xs, grandparents):
        avatar = await fetch_avatar(gp, avatar_size)
        paste_circle_avatar(image, avatar, (x, y_positions[0]), avatar_size)
    for x, p in zip(p_xs, parents):
        avatar = await fetch_avatar(p, avatar_size)
        paste_circle_avatar(image, avatar, (x, y_positions[1]), avatar_size)
    avatar_user = await fetch_avatar(user, avatar_size)
    paste_circle_avatar(image, avatar_user, (user_x, y_positions[2]), avatar_size)

    # --- Namen ---
    for x, gp in zip(g_xs, grandparents):
        draw_text_centered(draw, gp.display_name, x + avatar_size // 2, y_positions[0] + avatar_size + 12, font)
    for x, p in zip(p_xs, parents):
        draw_text_centered(draw, p.display_name, x + avatar_size // 2, y_positions[1] + avatar_size + 12, font)
    draw_text_centered(draw, user.display_name, user_x + avatar_size // 2, y_positions[2] + avatar_size + 12, font)

    output = io.BytesIO()
    image.save(output, format="PNG")
    output.seek(0)
    return output
