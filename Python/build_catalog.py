import os
import requests
import textwrap
import time
import lyricsgenius

# CONFIG
GENIUS_TOKEN = "PkuPzJNOymeOrzGSu8G-JMIep2yT9DHqbpXFfpnQzuAjmC71gyP2sGhNPBpYQLng" # Personal Token for Genius API
OUTPUT_DIR = "SD_CARD"
LCD_COLS   = 16
DELAY      = 1.5   # seconds between API calls (be polite to free API)
# ─────────────────────────────────────────────────────────────────────────────

genius = lyricsgenius.Genius(
    GENIUS_TOKEN,
    skip_non_songs=True,
    excluded_terms=["(Remix)","(Live)"],
    timeout = 15,
    retries = 3,
)


albums = [
    {"id": "001", "artist": "Ariana Grande",       "title": "Dangerous Woman"},
    {"id": "002", "artist": "Ariana Grande",       "title": "Thank U, Next"},
    {"id": "003", "artist": "Bad Bunny",           "title": "Debí Tirar Más Fotos"},
    {"id": "004", "artist": "Beyonce",             "title": "Lemonade"},
    {"id": "005", "artist": "Beyonce",             "title": "Renaissance"},
    {"id": "006", "artist": "Beyonce",             "title": "Cowboy Carter"},
    {"id": "007", "artist": "Billie Eilish",       "title": "Don't Smile at Me"},
    {"id": "008", "artist": "Billie Eilish",       "title": "When We All Fall Asleep, Where Do We Go?"},
    {"id": "009", "artist": "Billie Eilish",       "title": "Happier Than Ever"},
    {"id": "010", "artist": "Chappell Roan",       "title": "The Rise and Fall of a Midwest Princess"},
    {"id": "011", "artist": "Charli XCX",          "title": "Number 1 Angel"},
    {"id": "012", "artist": "Conan Gray",          "title": "Superache"},
    {"id": "013", "artist": "Fall Out Boy",        "title": "Mania"},
    {"id": "014", "artist": "Hayley Williams",     "title": "Petals for Armor"},
    {"id": "015", "artist": "Hayley Williams",     "title": "Flowers for Vases"},
    {"id": "016", "artist": "Hayley Williams",     "title": "Ego Death at a Bachelorette Party"},
    {"id": "017", "artist": "Josh Conway",         "title": "Plum"},
    {"id": "018", "artist": "Khalid",              "title": "American Teen"},
    {"id": "019", "artist": "Khalid",              "title": "Free Spirit"},
    {"id": "020", "artist": "Laufey",              "title": "Bewitched: The Goddess Edition"},
    {"id": "021", "artist": "Laufey",              "title": "A Night at the Symphony: Hollywood Bowl"},
    {"id": "022", "artist": "Lorde",               "title": "Pure Heroine"},
    {"id": "023", "artist": "Lorde",               "title": "Melodrama"},
    {"id": "024", "artist": "The Marias",          "title": "Superclean Vol. I"},
    {"id": "025", "artist": "The Marias",          "title": "Superclean Vol. II"},
    {"id": "026", "artist": "The Marias",          "title": "Cinema"},
    {"id": "027", "artist": "The Marias",          "title": "Submarine"},
    {"id": "028", "artist": "The Marias",          "title": "Nobody New"},
    {"id": "029", "artist": "The Marias",          "title": "Back to Me"},
    {"id": "030", "artist": "Michael Jackson",     "title": "Thriller"},
    {"id": "031", "artist": "My Chemical Romance", "title": "Three Cheers for Sweet Revenge"},
    {"id": "032", "artist": "My Chemical Romance", "title": "The Black Parade"},
    {"id": "033", "artist": "My Chemical Romance", "title": "The Black Parade Is Dead!"},
    {"id": "034", "artist": "Not For Radio",       "title": "Melt"},
    {"id": "035", "artist": "Not For Radio",       "title": "Bloom"},
    {"id": "036", "artist": "Olivia Rodrigo",      "title": "you seem pretty sad for a girl so in love"},
    {"id": "037", "artist": "Panic! at the Disco", "title": "A Fever You Can't Sweat Out"},
    {"id": "038", "artist": "Paramore",            "title": "All We Know Is Falling"},
    {"id": "039", "artist": "Paramore",            "title": "Riot!"},
    {"id": "040", "artist": "Paramore",            "title": "Decode"},
    {"id": "041", "artist": "Paramore",            "title": "I Caught Myself"},
    {"id": "042", "artist": "Paramore",            "title": "Brand New Eyes"},
    {"id": "043", "artist": "Paramore",            "title": "Paramore"},
    {"id": "044", "artist": "Paramore",            "title": "After Laughter"},
    {"id": "045", "artist": "Paramore",            "title": "This Is Why"},
    {"id": "046", "artist": "Pierce the Veil",     "title": "A Flair for the Dramatic"},
    {"id": "047", "artist": "Pierce the Veil",     "title": "Selfish Machines"},
    {"id": "048", "artist": "Pierce the Veil",     "title": "Collide with the Sky"},
    {"id": "049", "artist": "Pierce the Veil",     "title": "Misadventures"},
    {"id": "050", "artist": "Pierce the Veil",     "title": "The Jaws of Life"},
    {"id": "051", "artist": "Sabrina Carpenter",   "title": "Short n' Sweet (Deluxe)"},
    {"id": "052", "artist": "System of a Down",    "title": "System of a Down"},
    {"id": "053", "artist": "System of a Down",    "title": "Toxicity"},
    {"id": "054", "artist": "System of a Down",    "title": "Hypnotize"},
    {"id": "055", "artist": "Tyler, the Creator",  "title": "Igor"},
    {"id": "056", "artist": "Tyler, the Creator",  "title": "Call Me If You Get Lost"},
    {"id": "057", "artist": "Tyler, the Creator",  "title": "Chromakopia"},
    {"id": "058", "artist": "Wallows",             "title": "More"},
]

def fetch_tracklist(artist, title):
    """Fetch tracklist from MusicBrainz (free, no key needed)."""
    try:
        search_url = "https://musicbrainz.org/ws/2/release"
        params = {
            "query": f'release:"{title}" AND artist:"{artist}"',
            "fmt": "json",
            "limit": 1
        }
        headers = {"User-Agent": "VinylCatalog/1.0 (personal project)"}
        r = requests.get(search_url, params=params, headers=headers, timeout=10)
        releases = r.json().get("releases", [])
        if not releases:
            return []
        release_id = releases[0]["id"]
        time.sleep(1)
        detail_url = f"https://musicbrainz.org/ws/2/release/{release_id}"
        r2 = requests.get(detail_url, params={"fmt": "json", "inc": "recordings"}, headers=headers, timeout=10)
        data = r2.json()
        tracks = []
        for medium in data.get("media", []):
            for track in medium.get("tracks", []):
                tracks.append(track["title"])
        return tracks
    except Exception as e:
        print(f"    [tracklist error: {e}]")
        return []

def fetch_lyrics(artist, track):
    """Fetch lyrics from Genius"""
    try:
        song = genius.search_song(track, artist)
        if song and song.lyrics:
            # Clean up the lyrics Genius prepends (e.g. "SongName Lyrics\n")
            lyrics = song.lyrics.strip()
            first_newline = lyrics.find("\n")
            if first_newline != -1:
                first_line = lyrics[:first_newline]
                if "Lyrics" in first_line or "lyrics" in first_line:
                    lyrics = lyrics[first_newline:].strip()
            return lyrics
    except Exception as e:
        print(f"     [genius error: {e}]")
    return ""

def format_for_lcd(lyrics_text, cols=LCD_COLS):
    """Wrap lyrics to cols-wide lines, pair into 2-line frames separated by blank lines."""
    wrapped = []
    for line in lyrics_text.splitlines():
        line = line.strip()
        if not line:
            continue
        for chunk in textwrap.wrap(line, width=cols) or [line]:
            wrapped.append(chunk)
    frames = []
    for i in range(0, len(wrapped), 2):
        r1 = wrapped[i].ljust(cols)
        r2 = wrapped[i+1].ljust(cols) if i+1 < len(wrapped) else " " * cols
        frames.append(f"{r1}\n{r2}")
    return "\n\n".join(frames) + "\n"

def safe_folder_name(album_id):
    return f"ALB{album_id}"

# ── BUILD ─────────────────────────────────────────────────────────────────────
os.makedirs(OUTPUT_DIR, exist_ok=True)

# catalog.txt
with open(f"{OUTPUT_DIR}/catalog.txt", "w", newline="\n",encoding="utf-8") as f:
    for a in albums:
        f.write(f"{a['id']}|{a['title']}|{a['artist']}\n")
print(f"✓ catalog.txt written ({len(albums)} albums)")

# Per-album folders
for a in albums:
    folder = f"{OUTPUT_DIR}/{safe_folder_name(a['id'])}"
    os.makedirs(folder, exist_ok=True)
    print(f"\n[{a['id']}] {a['title']} — {a['artist']}")

    # Fetch tracklist
    tracks = fetch_tracklist(a["artist"], a["title"])
    time.sleep(DELAY)

    if not tracks:
        print("    ! No tracklist found — writing placeholder")
        tracks = ["(tracklist unavailable)"]

    with open(f"{folder}/tracklst.txt", "w", newline="\n", encoding="utf-8") as f:
        for i, t in enumerate(tracks, 1):
            f.write(f"{i:02d}|{t}\n")
    print(f"    ✓ tracklst.txt ({len(tracks)} tracks)")

    # Fetch lyrics for each track
    for i, track in enumerate(tracks, 1):
        fname = f"T{i:02d}.TXT"
        lyrics = fetch_lyrics(a["artist"], track)
        time.sleep(DELAY)

        if lyrics:
            content = format_for_lcd(lyrics)
            print(f"    ✓ {fname}  ({track})")
        else:
            content = f"Lyrics not\nfound      \n\n{track[:16].ljust(16)}\n{'by '+a['artist'][:13]}\n"
            print(f"    - {fname}  no lyrics ({track})")

        with open(f"{folder}/{fname}", "w", newline="\n", encoding="utf-8") as f:
            f.write(content)

print("\n\nDone! Copy the SD_CARD/ folder contents to your SD card.")
