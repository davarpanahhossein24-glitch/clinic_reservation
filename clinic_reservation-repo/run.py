from clinic_reservation.app import create_app

# ایجاد اپلیکیشن
app = create_app()

if __name__ == "__main__":
    # حالت debug برای توسعه محلی
    app.run(host="0.0.0.0", port=8000)
