from dope import db
from datetime import datetime

class Top100Songs(db.Model):
    SongTitle = db.Column(db.String(120), primary_key=True)
    Artist = db.Column(db.String(80), primary_key=True)
    NominatedBy = db.Column(db.String(80), primary_key=True)
    YesVotes = db.Column(db.Integer)
    NoVotes = db.Column(db.Integer)
    YesPercentage = db.Column(db.Float)
    AnachronismVotes = db.Column(db.Integer)
    
    def __init__(self, SongTitle, Artist, NominatedBy, YesVotes, NoVotes, AnachronismVotes, YesPercentage):
        self.SongTitle = SongTitle
        self.Artist = Artist
        self.NominatedBy = NominatedBy
        self.YesVotes = YesVotes
        self.NoVotes = NoVotes
        self.AnachronismVotes = AnachronismVotes
        self.YesPercentage = YesPercentage