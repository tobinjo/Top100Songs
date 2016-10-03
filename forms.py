from flask.ext.wtf import Form, validators

from wtforms import StringField, SelectField, TextField
from wtforms.validators import DataRequired
from models import Top100Songs


class SongSubmitForm(Form):
    
    SongName = StringField('openid', validators=[DataRequired()])
    Artist = StringField('Artist', validators=[DataRequired()])
    Nominator = StringField('Nominator', validators=[DataRequired()])
    
    def validate(self):
        rv = Form.validate(self)
        if not rv:
            return False
        
        song = Top100Songs.query.filter_by(SongTitle=self.SongName.data).first()
        if song is not None:
            return False
        
        return True