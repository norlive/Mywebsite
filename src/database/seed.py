from sqlalchemy.exc import SQLAlchemyError
import click

from src.models.portfolio import PortfolioItem, db

SAMPLE_PORTFOLIO_ITEMS = [
    {
        "title": "Project BBA",
        "src": "https://cdn.discordapp.com/attachments/1386369407260950599/1421503447802577107/image.png",
        "type": "image",
        "category": "Model + Rig",
        "description": "Sample render from the BBA collection."
    },
    {
        "title": "Project BBA2",
        "src": "https://cdn.discordapp.com/attachments/1386369407260950599/1420793520104538182/image.png",
        "type": "image",
        "category": "Model + Build",
        "description": "Alternate angle showcasing build details."
    },
    {
        "title": "Horse Animation",
        "src": "https://cdn.discordapp.com/attachments/1386369407260950599/1416799173667192853/2025-09-14_215248.mp4",
        "type": "video",
        "category": "Animation",
        "description": "Short motion study exported from BBA timeline."
    },
    {
        "title": "3D Model Showcase",
        "src": "https://cdn.discordapp.com/attachments/1424029054721327124/1424035359096049796/3e6da5ec-33bf-4281-98bf-b088aa1f6c9a_1.jpg",
        "type": "image",
        "category": "3D Model",
        "description": "High-poly sculpt with procedural texturing."
    },
    {
        "title": "Environment Fly-through",
        "src": "https://cdn.discordapp.com/attachments/1424029054721327124/1424035480189538304/image_4.png",
        "type": "image",
        "category": "Environment",
        "description": "Keyframe from an atmospheric lighting study."
    },
]


def seed_sample_portfolio():
    """Populate the portfolio table with sample data if empty."""
    if PortfolioItem.query.count() > 0:
        click.echo("Portfolio already contains data; skipping seed.")
        return

    try:
        for item in SAMPLE_PORTFOLIO_ITEMS:
            db.session.add(PortfolioItem(**item))
        db.session.commit()
        click.echo(f"Seeded {len(SAMPLE_PORTFOLIO_ITEMS)} portfolio items.")
    except SQLAlchemyError as exc:
        db.session.rollback()
        click.echo(f"Failed to seed portfolio items: {exc}", err=True)
        raise SystemExit(1)
