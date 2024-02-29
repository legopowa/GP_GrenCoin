import socket
import struct

# Curated list of server IPs, ports, and titles
SERVERS = [
    ("91.216.250.12", 27015, "Tf2 Skial test"),
    ("66.151.244.170", 27015, "-[EVIL]- TFC"),
    ("91.242.214.186", 27015, "1999tfc"),
    ("45.32.203.198", 27035, "OldSchool TFC"),
    ("172.93.101.194", 27015, "Drippy's TFC"),
    ("74.91.122.20", 27015, "TFPugs"),
    ("74.91.123.142", 27015, "TFPugs 2"),
    ("116.202.113.50", 27115, "Feckin-mad.co.uk"),
]

#known_players = ['illin', 'OST-CyKo Dad', 'Soldi', 'Frosty Baggins', 'Shergan', 'legopowa[tfc.fan dev]', 'Zima']
#known_players = [
#    "EveTheNight", "Majora", "FR35H", "NandoFH2", "Distruzio",
#    "Pong Lenis", "boris4000", "Buddeh", "_In_Sanity", "™™Shoebillionaire™™",
#    "Tunaman008", "Happy Tree Friends", "[SKVR] Iambic Pentameter", "blanketa",
#    "Dyson Dunbar", "Gramps with PTSD", "Kennnyyy", "misterjozo", "RossTizma",
#    "[TBR] ZeTROU", "Arrow", "DarkZoma", "poopertrooper", "Sanagi man",
#    "The FAKE Yukari", "Zaytun", "bunny ❤", "Bone", "bunk"
#]
known_players = [
    "olangmyr", "silvermetalindex", "TAGMANG", "Majora", "Pizza + Pepperoni",
    "Fubuki", "Jonny", "HamstaZ", "Big Ern", "Delphi",
    "poop machine", "❤❤Yachiyo Todoroki❤❤", "Axlle", "Bald Man", "CHIPS",
    "El Toad", "Eva_Unit01", "O'Malley de Bough", "Sirius", "Filthy Hope",
    "Flaky", "non", "PhoenixIsFallen", "HOT BEEF INJECTION", "Largeish Beans",
    "robespierre", "Bucknasty", "Loki", "Noxus", "Yeb AFK",
    "Jeffafa AFK", "not a fed", "legopowa"
]






def send_udp_request(ip, port, message):
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(2)
        try:
            sock.sendto(message, (ip, port))
            response, _ = sock.recvfrom(4096)
            return response
        except socket.timeout:
            print(f"Request to {ip}:{port} timed out")
            return None

def get_challenge_number(ip, port):
    challenge_request = b'\xFF\xFF\xFF\xFF\x55\xFF\xFF\xFF\xFF'
    response = send_udp_request(ip, port, challenge_request)
    if response and response[4] == 0x41:
        return response[5:]
    return None

def find_known_players(response):
    found_players = set()
    for player in known_players:
        if player in response:
            found_players.add(player)
    return found_players

def get_player_list(ip, port, title, challenge):
    player_request = b'\xFF\xFF\xFF\xFF\x55' + challenge
    response = send_udp_request(ip, port, player_request)
    
    if response:
        # Decode response to string for keyword searching
        decoded_response = response.decode('utf-8', errors='ignore')
        players = find_known_players(decoded_response)
        print(f"Known players on {ip}:{port} - {title}: {players}")

def main():
    for ip, port, title in SERVERS:
        print(f"Querying server: {title} at {ip}:{port}")
        challenge = get_challenge_number(ip, port)
        if challenge:
            get_player_list(ip, port, title, challenge)

if __name__ == "__main__":
    main()
