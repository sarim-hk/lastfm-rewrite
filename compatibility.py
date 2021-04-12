import urllib.request
import json

class User:
    def __init__(self, username, LASTFM_KEY, timeframe="overall"):
        self._username = username
        self._timeframe = timeframe
        self._top_artists = self.get_top_artists(LASTFM_KEY)
        self._total = self.get_total_plays(LASTFM_KEY)

    def get_top_artists(self, LASTFM_KEY):
        url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={self._username}&period={self._timeframe}&api_key={LASTFM_KEY}&limit=100&format=json"
        with urllib.request.urlopen(url) as url:
            data = json.load(url) #loaded as dict
        return data["topartists"]["artist"]

    def get_total_plays(self, LASTFM_KEY):
        url = f"http://ws.audioscrobbler.com/2.0/?method=user.gettopartists&user={self._username}&period={self._timeframe}&api_key={LASTFM_KEY}&limit=100&format=json"
        with urllib.request.urlopen(url) as url:
            data = json.load(url) #loaded as dict
        return int(data["topartists"]["@attr"]["total"])


parabola = lambda y : 4.3*(200-2*y)**.5

turn_to_percentage = lambda score : (score*100)/196

def score_data(user1, user2):
    score = 0
    count = 0

    for x in user1._top_artists:
        count += 1
        for y in user2._top_artists:
            if x["name"] == y["name"]:
                score += parabola(int(x["@attr"]["rank"]))
                break
    return score/count


if __name__ == "__main__":
    with open("resources/keys.txt", "r") as f:
        LASTFM_KEY = f.readline().split("=")[1].strip("\n")
    timeframe = "overall"

    user1, user2 = User("shktv", LASTFM_KEY), User("shktv", LASTFM_KEY)
    score = (score_data(user1, user2) + score_data(user2, user1)) / 2
    print(score)
    print("\n\n\n")
    print(int(score*1000)/402)
