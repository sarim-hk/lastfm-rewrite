def register(user_id, username):
    with open("register.txt", "a") as f:
        f.write(f"{user_id}|{username}")

def id_to_username(user_id):
    with open("register.txt", "r") as f:
        lines = f.readlines()
        lines.reverse()

    for entry in lines:
        entry = entry.split("|")
        if entry[0] == str(user_id):
            return entry[1]
    return None
