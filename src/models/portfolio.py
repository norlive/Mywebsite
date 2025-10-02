from src.models.user import db

class PortfolioItem(db.Model):
    __tablename__ = 'portfolio_items'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    src = db.Column(db.String(500), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # 'image' or 'video'
    category = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    def to_dict(self):
        return {
            'id': str(self.id),
            'title': self.title,
            'src': self.src,
            'type': self.type,
            'category': self.category,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

