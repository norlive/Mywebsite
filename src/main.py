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
                src="https://cdn.discordapp.com/attachments/1391280671703437322/1420329864577286224/image.png?ex=68e0de44&is=68df8cc4&hm=da583bfe506b4b6b71b4e349da8b48f82558bd1f5c48a50efc8f4911883e2222&",
                type="image",
                category="Model + Rig",
                description=""
            ),
            PortfolioItem(
                title="Project BBA2",
                src="https://cdn.discordapp.com/attachments/1391280671703437322/1419875248509157396/image.png?ex=68e0885f&is=68df36df&hm=dd5eec90998dd33c747906e37f56fd19494248236d017a508ebb2187f296dcec&",
                type="image",
                category="Model + Rig",
                description=""
            ),
            PortfolioItem(
                title="UGC ITEM",
                src="https://cdn.discordapp.com/attachments/1391280671703437322/1420821547031199856/image.png?ex=68e0adee&is=68df5c6e&hm=a12783cf1c9d995c7a248e5e32e2d2ea6839848fb48479602f0607de8791abd2&",
                type="image",
                category="Model",
                description="A sleek web design project."
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
