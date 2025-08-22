import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch

cid = '56f5940b65e94d7196e42d20756d0ce0'
secret = '922d9068a4c34f4485579d54cdfd7823'
redirect_uri = 'http://127.0.0.1:8888/callback'

# Cần scope để đọc playlist
scope = "playlist-read-private playlist-read-collaborative"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    client_id=cid,
    client_secret=secret,
    redirect_uri=redirect_uri,
    scope=scope,
    show_dialog=True  # luôn hiển thị đăng nhập mỗi lần chạy
))
def check_playlist_access(playlist_id):
    try:
        playlist = sp.playlist(playlist_id)
        print(f"🎧 Playlist: {playlist['name']}")
        print(f"👥 Owner: {playlist['owner']['display_name']}")
        print(f"🔓 Public: {playlist['public']}")
        print(f"📦 Số bài hát: {playlist['tracks']['total']}")
    except Exception as e:
        print(f"❌ Không thể truy cập playlist ID '{playlist_id}':\n{e}")

# check_playlist_access("4mIAUiKonMlqgWtMeyt1ZM")
if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Dùng: python connect.py <playlist_id>")
        print("Ex: python connect.py 4mIAUiKonMlqgWtMeyt1ZM")
    else:
        playlist_id = sys.argv[1]
        check_playlist_access(playlist_id)


# chạy:  python connect.py <playylist_id trên spotify>    để test xem có tải được id không