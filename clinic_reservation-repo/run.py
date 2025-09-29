from clinic_reservation import create_app

# اپلیکیشن باید همیشه ساخته بشه (چه لوکال، چه روی سرور)
app = create_app()

if __name__ == "__main__":
    # فقط برای اجرای لوکال (نه روی Render)
    app.run(host="0.0.0.0", port=8000, debug=True)

