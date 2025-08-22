import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from youtubesearchpython import VideosSearch
import os
import json
import yt_dlp
from pydub import AudioSegment

cid = '56f5940b65e94d7196e42d20756d0ce0' #insert your own id
secret = '922d9068a4c34f4485579d54cdfd7823'

# Kết nối với Spotify API
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(
    client_id=cid,
    client_secret=secret,
))

# Tìm link YouTube dựa trên tên bài hát
def get_youtube_link(song_title, artist_name):
    query = f"{song_title} {artist_name} audio"
    videosSearch = VideosSearch(query, limit=1)
    result = videosSearch.result()
    if result["result"]:
        return result["result"][0]["link"]
    return None

def get_link(url,save_file_path):
    import time

    playlist_link = f"https://open.spotify.com/playlist/{url}?si=f819917d1bca45b8"
    playlist_id = playlist_link.split("/")[-1].split("?")[0]

    youtube_links = []
    offset = 0
    limit = 100

    while True:
        tracks = sp.playlist_tracks(playlist_id, offset=offset, limit=limit)
        items = tracks['items']
        if not items:
            break  # hết bài

        for item in items:
            track = item['track']
            if not track:
                continue
            name = track['name']
            artist = track['artists'][0]['name']
            yt_link = get_youtube_link(name, artist)
            youtube_links.append((name, artist, yt_link))
            print(f"✅ {name} - {artist} → {yt_link}")
            time.sleep(0.1)  # tránh bị rate limit

        offset += limit

    # Ghi toàn bộ kết quả vào file
    with open(save_file_path, "a", encoding="utf-8") as f:
        for name, artist, link in youtube_links:
            f.write(f"{name} - {artist}: {link}\n")
  

# count mussic in file txt 
def count_lines(file_path):
      # file_path = "/content/drive/MyDrive/api Spotify/youtube_links_bolero.txt"  
      with open(file_path, 'r', encoding='utf-8') as f:
          line_count = sum(1 for _ in f)

      print(f"📄 Số dòng trong file '{file_path}': {line_count}")


# clean duplicate and rm remix 
def clean_data(input_file):
    seen_links = set()
    cleaned_lines = []

    with open(input_file, "r", encoding="utf-8") as f:
        for line in f:
            line_lower = line.lower()
            if "remix" in line_lower or "Remix" in line_lower:
                continue  

            if ':' not in line:
                continue  # bỏ dòng sai định dạng

            try:
                _, link = line.strip().split(':', 1)
                link = link.strip()

                if link in seen_links:
                    continue  # bỏ dòng nếu link đã xuất hiện

                seen_links.add(link)
                cleaned_lines.append(line.strip())
            except Exception as e:
                print(f"⚠️ Lỗi xử lý dòng: {line.strip()}")

    # Ghi lại kết quả đã lọc
    with open(input_file, "w", encoding="utf-8") as f:
        for line in cleaned_lines:
            f.write(line + "\n")

    print(f"Đã lưu {len(cleaned_lines)} dòng sạch vào: {input_file}")





def download_and_convert_youtube(link, save_path_wav):
    temp_file = save_path_wav.replace('.wav', '')

    ydl_opts = {
    'format': 'bestaudio/best',
    'outtmpl': temp_file,
    'quiet': True,
    'cookiefile': 'cookie.txt' # file content cookie youtube
    }
    ydl_opts_info = {
        'quiet': True,
        'skip_download': True,
        'cookiefile': 'cookie.txt'
    }
    try:
        # bỏ qua nếu video dài hơn 10'
        with yt_dlp.YoutubeDL(ydl_opts_info) as ydl:
            info = ydl.extract_info(link, download=False)
            duration = info.get("duration", 0) 

            if duration > 600:
                print(f"video dài hơn 10 phút: {link} ({duration // 60} phút)")
                return
        # dowload wav
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            print(f"🎵 Đang tải: {link}")
            ydl.download([link])

        if not os.path.exists(temp_file):
            raise FileNotFoundError(f" Không tìm thấy file tạm: {temp_file}")

        audio = AudioSegment.from_file(temp_file)
        audio = audio.set_channels(1).set_frame_rate(16000)
        audio.export(save_path_wav, format="wav")
        os.remove(temp_file)
        print(f" Đã lưu: {save_path_wav}")
    except Exception as e:
        print(f" Lỗi với {link}: {e}")

# Đọc file youtube_links.txt (dạng: Tên bài - Ca sĩ: link)
def read_file_and_download(file_path,save_path):
    with open(file_path, "r", encoding="utf-8") as f:
        for line in f:
            try:
                if ':' not in line:
                    print(f" Dòng không hợp lệ: {line.strip()}")
                    continue

                title, link = line.strip().split(':', 1)
                link = link.strip()
                print("dowload:",link)  

                song_name = (
                    title.strip()
                    .replace(" - ", "_")
                    .replace(" ", "_")
                    .replace("/", "_")
                    .replace("\\", "_")
                    .replace("(", "")
                    .replace(")", "")
                    .replace(":", "")
                )
                save_path_wav = os.path.join(save_path, f"{song_name}.wav")
                if not os.path.exists(save_path_wav):
                    download_and_convert_youtube(link, save_path_wav)
            except Exception as e:
                print(f" Không thể xử lý dòng: {line}\nLỗi: {e}")

def preprocep_data(json_list,save_path):
    os.makedirs(save_path, exist_ok=True)
  #  write link to file txt
    for item in json_list:
            name = item['name']
            os.makedirs(f"{save_path}/{name}", exist_ok=True)
            save_file_path=f"{save_path}/{name}"
            file_link = f"{save_file_path}/youtube_links_{name}.txt"
            if not os.path.exists(file_link):
                with open(file_link, "w", encoding="utf-8") as f:
                    pass
            for url in item['url']:
                try:
                   print(f"đang viết vào:{file_link}")
                   get_link(url,file_link)
                   print(f"Đã lưu vào: {file_link}")
                except Exception as e:
                  print(f"Lỗi với url {url} trong playlist '{name}': {e}")
            clean_data(file_link)
            read_file_and_download(file_link,save_file_path)
            print("ok")

#  run 
#  json list là file json các id list bài hát để tải 
# json_list = json.load(open("json_list.json"))
json_list =[
    # {
    #     "name": "bolero",
    #     "url":["0Gi20HOQSsgzbmTL9zthTI"]
    # },
    # {
    #     "name": "pop",
    #     "url":["0aiBKNSqiPnhtcw1QlXK5s"]
    # },
    {
        "name": "dan ca",
        "url":["4pOgYiQ33mfBpnDgte8hPt"]
    },
]

# read_file_and_download(r"D:\classified_music\data_test\bolero\youtube_links_bolero.txt",r'D:\classified_music\data_test\bolero')
preprocep_data(json_list,r"D:\classified_music\data_test")     