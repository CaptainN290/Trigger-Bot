from PIL import Image, ImageDraw, ImageFont
import os

CARD_WIDTH = 600
CARD_HEIGHT = 400
CARD_COLOR = (26, 188, 156)  # turquoise
TEXT_COLOR = (255, 255, 255)
FONT_PATH = "arial.ttf"  # use system font or add a ttf in your folder

TEMP_FOLDER = "temp_profiles"
os.makedirs(TEMP_FOLDER, exist_ok=True)


def generate_profile_card(
    username, avatar_path, trion, side_effect,
    spins, credits, elo, wins, losses,
    stats, triggers, story_arc, story_mission, user_id
):
    # Delete old profile if exists
    temp_file = os.path.join(TEMP_FOLDER, f"{user_id}.png")
    if os.path.exists(temp_file):
        os.remove(temp_file)

    card = Image.new("RGB", (CARD_WIDTH, CARD_HEIGHT), CARD_COLOR)
    draw = ImageDraw.Draw(card)

    # Load font
    try:
        font_title = ImageFont.truetype(FONT_PATH, 28)
        font_small = ImageFont.truetype(FONT_PATH, 18)
    except:
        font_title = ImageFont.load_default()
        font_small = ImageFont.load_default()

    # Draw avatar
    avatar = Image.open(avatar_path).convert("RGBA").resize((100, 100))
    mask = Image.new("L", avatar.size, 0)
    draw_mask = ImageDraw.Draw(mask)
    draw_mask.ellipse((0, 0, 100, 100), fill=255)
    card.paste(avatar, (20, 20), mask)

    # Username
    draw.text((140, 20), username, fill=TEXT_COLOR, font=font_title)

    # Trion & Side Effect
    draw.text((140, 60), f"🔋 Trion: {trion}", fill=TEXT_COLOR, font=font_small)
    draw.text((140, 85), f"🧬 Side Effect: {side_effect or 'None'}", fill=TEXT_COLOR, font=font_small)

    # Spins & Credits
    draw.text((140, 110), f"🎰 Spins: {spins}   💳 Credits: {credits}", fill=TEXT_COLOR, font=font_small)

    # ELO & Wins/Losses
    draw.text((140, 135), f"🏆 ELO: {elo}   Wins/Losses: {wins}/{losses}", fill=TEXT_COLOR, font=font_small)

    # Stats
    stat_y = 170
    for stat_name, value in stats.items():
        draw.text((20, stat_y), f"🔹 {stat_name}: {value}", fill=TEXT_COLOR, font=font_small)
        stat_y += 25

    # Triggers
    trigger_text = " | ".join(triggers) if triggers else "None"
    draw.text((20, stat_y + 10), f"🎯 Triggers: {trigger_text}", fill=TEXT_COLOR, font=font_small)

    # Story Progress
    draw.text((20, stat_y + 35), f"📖 Story: {story_arc} → {story_mission}", fill=TEXT_COLOR, font=font_small)

    # Save card
    card.save(temp_file)
    return temp_file
