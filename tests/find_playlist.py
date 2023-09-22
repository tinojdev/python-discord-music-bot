from yt_dlp import YoutubeDL

ytdlp = YoutubeDL(
    params={"extract_flat": "in_playlist", "skip-download": True, "verbose": True}
)
info = ytdlp.extract_info(
    "https://www.youtube.com/watch?v=sAX4qreYRv4&list=PLPy6Ka57myt782w17YOhrAI1yXx79u6vC",
    download=False,
    extra_info={"flat_playlist": True},
)
if info is None:
    print("No playlist found")
else:
    print(list(map(lambda x: x["url"], info["entries"])))
