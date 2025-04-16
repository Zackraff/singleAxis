from app import app
from app.controller.firebaseController import sync_data_from_fb_to_postgres

sync_data_from_fb_to_postgres()

if __name__ == "_main_":
    app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)