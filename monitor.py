import requests, hashlib, os

# 監視対象候補者の一覧
candidates = {
    "河村建一":     "https://go2senkyo.com/seijika/183125",
    "なかしま里奈": "https://go2senkyo.com/seijika/196353",
    "坂本まさし":   "https://go2senkyo.com/seijika/196345",
    "じんむら浩平": "https://go2senkyo.com/seijika/195636",
    "くれよしつぐ": "https://go2senkyo.com/seijika/196111",
    "望月まさのり": "https://go2senkyo.com/seijika/191999",
    "とりうみあや": "https://go2senkyo.com/seijika/196112",
    "たかく則男":   "https://go2senkyo.com/seijika/18558",
    "高野たかひろ": "https://go2senkyo.com/seijika/195381",
    "あべ 力也":    "https://go2senkyo.com/seijika/12888",
    "里吉ゆみ":     "https://go2senkyo.com/seijika/12866",
    "三宅 しげき":  "https://go2senkyo.com/seijika/77084",
    "福島 りえこ":  "https://go2senkyo.com/seijika/165090",
    "風間 ゆたか":  "https://go2senkyo.com/seijika/18554",
    "高岡 じゅん子":"https://go2senkyo.com/seijika/30954",
    "平井 しげる":  "https://go2senkyo.com/seijika/196580",
    "ク ガイ":      "https://go2senkyo.com/seijika/196661",
}

def main():
    updates = []
    os.makedirs("hashes", exist_ok=True)

    for name, url in candidates.items():
        response = requests.get(url)
        content = response.text
        hash_now = hashlib.sha256(content.encode("utf-8")).hexdigest()

        hash_file = f"hashes/{name}.txt"
        old_hash = None

        if os.path.exists(hash_file):
            with open(hash_file, "r") as f:
                old_hash = f.read()

        if old_hash != hash_now:
            if old_hash:  # 初回除外
                updates.append(f"{name} のページが更新されました → {url}")
            with open(hash_file, "w") as f:
                f.write(hash_now)

    if updates:
        print("✅ 更新が検出されました：\n" + "\n".join(updates))
    else:
        print("🔍 変更はありませんでした。")

if __name__ == "__main__":
    main()
