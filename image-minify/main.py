import io, os, time
from flask import Flask, render_template, request, send_file, redirect, url_for, flash
from PIL import Image
from collections import defaultdict

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-key')


USAGE = defaultdict(list)

FREE_LIMIT_PER_DAY = 3

def can_use_free(ip):
    now = time.time()
    day_ago = now - 24*3600
    USAGE[ip] = [t for t in USAGE[ip] if t > day_ago]
    return len(USAGE[ip]) < FREE_LIMIT_PER_DAY

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        ip = request.headers.get('X-Forwarded-For', request.remote_addr)
        plan = request.form.get("plan", "free")

        if plan == "free" and not can_use_free(ip):
            flash("سهمیه رایگان امروزت تموم شده.پلن pro رو فعال کن تا نامحدود استفاده کنی")
            return redirect(url_for('index'))

        f = request.files.get('image')
        if not f or f.filename == '':
            flash("لطفا یک تصویر انتخاب کن")
            return redirect(url_for('index'))

        try:
            img = Image.open(f.stream).convert('RGB')

            target_width = request.form.get("width", type=int)
            quality = request.form.get("quality", type=int) or 80

            if target_width and target_width > 0 and img.width > target_width:
                ratio = target_width / float(img.width)
                target_height = int(img.height * ratio)
                img = img.resize((target_width, target_height), Image.LANCZOS)

            buf = io.BytesIO()
            img.save(buf, format='WEBP', quality=quality, method=6)
            buf.seek(0)

            if plan == "free":
                ip = request.headers.get('X-Forwarded-For', request.remote_addr)
                USAGE[ip].append(time.time())

            filename = "output.webp"
            return send_file(
                buf,
                mimetype='image/webp',
                as_attachment=True,
                download_name=filename,
            )
        except Exception as e:
            print("Error: ", e)
            flash("خطا در پردازش تصویر. لطفا دوباره امتحان کن.")
            return redirect(url_for('index'))

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)