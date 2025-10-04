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
            # New items (3D Model Images)
            PortfolioItem(
                title="3D Model 1",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424035359096049796/3e6da5ec-33bf-4281-98bf-b088aa1f6c9a_1.jpg?ex=68e27bc6&is=68e12a46&hm=b64fe5a6b457c8edca536b907f479fabf9a96b21f4c11528d27959e87659147d&",
                type="image",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model 2",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424035359553224925/509440653_1885408352002679_5690689316477236266_n_1.jpg?ex=68e27bc7&is=68e12a47&hm=8d8dcc57fab259bb696e085c98f1d50143282f93e0fd3f734ef49e1237b49d2e&",
                type="image",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model 3",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424035359964139700/4e60a37e-6b3b-4ff4-b29a-260eb1a23409_1.jpg?ex=68e27bc7&is=68e12a47&hm=eb20d88f2f580c494d5a28fa71ce965ba6801073a840eb28d50bdfeceb55e095&",
                type="image",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model 4",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424035360274649318/5cd129bb-ad1d-4cf2-b12b-220a3d63d457_1.jpg?ex=68e27bc7&is=68e12a47&hm=fe60631fb20673004213511911a8d46f46923d1250bf75f483bc01389535e7b3&",
                type="image",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model 5",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424035360597606400/2025-08-29_175401.png?ex=68e27bc7&is=68e12a47&hm=d4be14ef3ea770291db55a7bc99482c2bd0e98caa7a121146a4836266d57b9ca&",
                type="image",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model 6",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424035480189538304/image_4.png?ex=68e27be3&is=68e12a63&hm=a49c9e66699f8ddc984bed5414bb310a35c4cbae60602ab348bcf3c329f67f5b&",
                type="image",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model 7",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424035483062898770/55_1.png?ex=68e27be4&is=68e12a64&hm=351805b35c1984ac1a9907d6dd5647c67543b8efb078b80eb9842697d707b657&",
                type="image",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model 8",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424035482354057307/66_1.png?ex=68e27be4&is=68e12a64&hm=6ebef7ce9d6a3682ee8e993c12d0c52397e0397b894c81dbff9a39ac9a5d5b41&",
                type="image",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model 9",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424035168976633970/5468_1.png?ex=68e27b99&is=68e12a19&hm=29ac3c987b0f07fd863675add88060dbbd1d3a09dae9854b7ea5e0ec6fc58af0&",
                type="image",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036229007016076/1.MP4_1_1.mp4?ex=68e27c96&is=68e12b16&hm=55d9c940c5dd3c2f2acebde8998e31b6bf2f34f1db2f21eb186d10ea95293219&",
                type="video",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036218559004802/AQMtkGf9c591VP0p8aQPUS9oueUIOXQPMSW0dcE9_kB-MwCMtkno-4Kmu6wcpd30wFIfU__elOQM9WthxBEiQXgJ_1.mp4?ex=68e27c93&is=68e12b13&hm=f7bb51c20209bcdbee6e54cce4e3102cb5515ed1c0b18f4c53427e65020dda83&",
                type="video",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036207280656414/Roblox-2025-08-04T02_55_52.231Z_1_1.mp4?ex=68e27c91&is=68e12b11&hm=3cf6904d3e3b6653353f331cd2b5cdff7f628bd7c3b96c157414065c1e5ea99d&",
                type="video",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036101386928298/AQNQk_Deqyz00F2KMi1x8c45VKRnrxqtcowvB-Tu1F2CN_DaqQSE96HjyJs_M3jw5Hz6ZLgwG9XUi4LZV6Ekf4xOvw9W-tZMKvrz0UoPRnvhbQ_1.mp4?ex=68e27c77&is=68e12af7&hm=cedd9acfa949df34598b98b07a8c73cc787fe2adcbb7601659bce0542dec449b&",
                type="video",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036065362055219/7698ca7b8d4a40a690af724c48014b93_1.mov?ex=68e27c6f&is=68e12aef&hm=19adb1acff55b4443696635523c4fb2b233c64f352d33d2e46811aa657052b97&",
                type="video",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036561330110474/0001-0250_5_1.mp4?ex=68e27ce5&is=68e12b65&hm=6d552b9a4ae20e379828b6482ee430403ab9e28a9c1d422d8e3eae4f4823be43&",
                type="video",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036580221259946/0001-0250_6_1.mp4?ex=68e27cea&is=68e12b6a&hm=ef504a2a403a773de2372260bf31ca202c87409e52220f43edce2ebc8c40ba2d&",
                type="video",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036600953700523/0001-0250_8_1.mp4?ex=68e27cee&is=68e12b6e&hm=c8bd9b85a2ae9d64af84235ef4e457bf7511fe04b8fcb8fe13e28feb8d091809&",
                type="video",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036601599758356/0001-0250_4_1.mp4?ex=68e27cef&is=68e12b6f&hm=ebfcb92a531c9a290ef9ecab073fddceea239976a9dd02e24a0ab4fb0c943408&",
                type="video",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036619765420092/0001-0250_1_1.mp4?ex=68e27cf3&is=68e12b73&hm=21f90ac0e9c1cf2dce77c17b479b8aa32320c4aed8ec30aba752f1883533a208&",
                type="video",
                category="3D Model",
                description=""
            ),
            PortfolioItem(
                title="3D Model",
                src="https://cdn.discordapp.com/attachments/1424029054721327124/1424036620247629995/0001-0250_3_1.mp4?ex=68e27cf3&is=68e12b73&hm=6821377ac06e600f2def38b6e917ecd26aec782b82bfb1fcd63ac6386eb92db6&",
                type="video",
                category="3D Model",
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
