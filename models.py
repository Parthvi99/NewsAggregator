from FlaskPage import ourdb as db


class RssLinks(db.Model):
    """Data model for RSS links."""

    __tablename_ = 'main_rss'

    id = db.Column(
        db.Integer,
        primary_key=True,
        autoincrement=True
    )

    main_links = db.Column(
        db.String(255),
        unique=True,
        nullable=False
    )

    def __repr__(self):
        return '<RssLinks {}>'.format(self.id)
