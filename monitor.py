import requests, hashlib, os, smtplib
from email.mime.text import MIMEText

# 通知先メールアドレス
TO_EMAIL = "kaga.shinya@tsunag-i.com"
FROM_EMAIL = "no-reply@example.com"

# GitHub ActionsのSecretsに登録した環境変数名
SMTP_HOST     = os.getenv("SMTP_HOST")
SMTP_PORT     = int(os.getenv("SMTP_PORT", 587))
SMTP_USER     = os.getenv("SMTP_USER")
SMTP_PASSWORD = os.getenv("SMTP_PASSWORD")

# 監視対象候補者一覧
candidates = {
    "河村建一":     "https://go2senkyo.com/seijika/183125",
    "なかしま里奈": "https://go2senkyo.com/seijika/196353",
    "坂本まさし":   "https://go2senkyo.com/seijika/196345",
    "じんむら浩平": "https://go2senkyo.com/seijika/195636",
    "くれよしつぐ": "https://go2senkyo.com/seijika/196111",
    "望月まさのり": "https://go2senkyo.com/seijika/191999",
    "とりうみあや": "https://go2senkyo.com/seijika/196112",
    "たかく則男":   "https://go2senkyo.com/seijika/18558",
    "高野たかひろ":"https://go2senkyo.com/seijika/195381",
    "あべ 力也":    "https://go2senkyo.com/seijika/12888",
    "里吉ゆみ":     "https://go2senkyo.com/seijika/12866",
    "三宅 しげき":  "https://go2senkyo.com/seijika/77084",
    "福島 りえこ":  "https://go2senkyo.com/seijika/165090",
    "風間 ゆたか":  "https://go2senkyo.com/seijika/18554",
    "高岡 じゅん子":"https://go2senkyo.com/seijika/30954",
    "平井 しげる":  "https://go2senkyo.com/seijika/196580",
    "小松 大祐":  "https://go2senkyo.com/seijika/30953",
    "ク ガイ":      "https://go2senkyo.com/seijika/196661",
}

def send_email(subject, body):
    msg = MIMEText(body, _charset="utf-8")
    msg["Subject"] = subject
    msg["From"] = FROM_EMAIL
    msg["To"] = TO_EMAIL

    with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as smtp:
        smtp.starttls()
        smtp.login(SMTP_USER, SMTP_PASSWORD)
        smtp.send_message(msg)

def main():
    updates = []

    for name, url in candidates.items():
        r = requests.get(url, timeout=10)
        content = r.text
        current_hash = hashlib.sha256(content.encode("utf-8")).hexdigest()
        fn = f"hash_{name}.txt"

        old = None
        if os.path.exists(fn):
            with open(fn, "r") as f:
                old = f.read().strip()

        if old != current_hash and old is not None:
            updates.append((name, url))

        with open(fn, "w") as f:
            f.write(current_hash)

    if updates:
        body = "\n".join([f"・{name} のページが更新されました：{url}" for name, url in updates])
        subject = "【更新通知】選挙ドットコム候補者ページ"
        send_email(subject, body)
        print(body)

if __name__ == "__main__":
    main()
