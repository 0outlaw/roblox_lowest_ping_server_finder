import requests, pyperclip

while True:
    game_id = input("game id: ")
    if game_id.isdigit():
        game_id_status_code = requests.get(f"https://www.roblox.com/games/{game_id}/").status_code
        if game_id_status_code == 404:
            print("invalid game id")
            continue
        else:
            break
    else:
        print("game id format incorrect")
        continue

servers_data = []
def get_servers(next_page_cursor = ""):
    server_data = requests.get(f"https://games.roblox.com/v1/games/4282985734/servers/Public?limit=100&cursor={next_page_cursor}").json()
    for main_server_data in server_data.get("data"):
        servers_data.append({"id": main_server_data.get("id"), "ping": main_server_data.get("ping")})
    if server_data.get("nextPageCursor") is not None:
        next_next_page_cursor = server_data.get("nextPageCursor")
        print(next_next_page_cursor)
        return get_servers(next_next_page_cursor)


get_servers()

minimum_server_data = min(servers_data, key = lambda server_data: server_data.get("ping"))
pyperclip.copy(f"Roblox.GameLauncher.joinGameInstance({game_id}, '{minimum_server_data.get('id')}')")
