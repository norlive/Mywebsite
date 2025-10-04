import os
import sys
# DON'T CHANGE THIS !!!
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, send_from_directory
from flask_cors import CORS
from src.models.user import db
from src.models.portfolio import PortfolioItem
from src.routes.user import user_bp
from src.routes.portfolio import portfolio_bp

app = Flask(__name__, static_folder=os.path.join(os.path.dirname(__file__), 'static'))
app.config['SECRET_KEY'] = 'asdf#FGSgvasgf$5$WGT'

# Enable CORS for all routes
CORS(app)

app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(portfolio_bp, url_prefix='/api')

# uncomment if you need to use database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(os.path.dirname(__file__), 'database', 'app.db')}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)
with app.app_context():
    db.create_all()
    
    # Add sample data if no items exist
    if PortfolioItem.query.count() == 0:
        sample_items = [
            PortfolioItem(
                title="Project BBA",
                src="https://cdn.discordapp.com/attachments/1386369407260950599/1421503447802577107/image.png?ex=68e1d780&is=68e08600&hm=cae075f75748adaf1f894c0be80d4a7d396b1cce9604a141f9962aeff3730be8&",
                type="image",
                category="Model + Rig",
                description=""
            ),
            PortfolioItem(
                title="Project BBA2",
                src="https://cdn.discordapp.com/attachments/1386369407260950599/1420793520104538182/image.png?ex=68e1e554&is=68e093d4&hm=e936dddc637e7b36475de55433ec265a0aa7001d6c5fea3f2e2a221adb9aec9f&",
                type="image",
                category="Model + Build",
                description=""
            ),
            PortfolioItem(
                title="Horse Animation",
                src="https://cdn.discordapp.com/attachments/1386369407260950599/1416799173667192853/2025-09-14_215248.mp4?ex=68e1ddcd&is=68e08c4d&hm=79e19a2e48e6dc0ef8405c305f377601bdc26e7c1df978897875bff83ea18b9e&",
                type="video",
                category="Animation",
                description=""
            ),
            PortfolioItem(
                title="Test",
                src="https://drive.google.com/file/d/1DkMOlsIe0SyDRvJGGQg_cQtxoMcoyrkF/view?usp=sharing",
                type="image",
                category="Animation",
                description=""
            )
        ]
        
        for item in sample_items:
            db.session.add(item)
        db.session.commit()

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    static_folder_path = app.static_folder
    if static_folder_path is None:
            return "Static folder not configured", 404

    if path != "" and os.path.exists(os.path.join(static_folder_path, path)):
        return send_from_directory(static_folder_path, path)
    else:
        index_path = os.path.join(static_folder_path, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(static_folder_path, 'index.html')
        else:
            return "index.html not found", 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
