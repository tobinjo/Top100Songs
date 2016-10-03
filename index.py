from flask import Flask, render_template, flash, request, session
from flask.ext.sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)
app.config.from_object('config')

app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['DATABASE_URL']
db = SQLAlchemy(app)

#app.secret_key =
#Omitted for security reasons.

@app.route('/Top100Songs', methods=['GET', 'POST'])
def display():
    from forms import SongSubmitForm
    from models import Top100Songs
    form = SongSubmitForm()
    if form.validate_on_submit():
        song1 = Top100Songs(form.SongName.data, form.Artist.data, form.Nominator.data, 1, 0, 0, 100)
        db.session.add(song1)
        db.session.commit()
        flash('Successfully submitted the song: %s by %s' % (form.SongName.data, form.Artist.data))
    else:
        flash('The song: %s by %s already exists in the database' % (form.SongName.data, form.Artist.data))
    
    return render_template('submit.html', form=form)

@app.route('/ViewSongs')
def ViewSongs():
    from models import Top100Songs
    SongTable = Top100Songs.query.order_by(Top100Songs.YesPercentage.desc()).limit(100)
    return render_template('ViewSongs.html', SongTable=SongTable)

@app.route('/Vote', methods=['GET', 'POST'])
def Vote():
    from models import Top100Songs
    from forms import VoteForm
    form = VoteForm()
    
    if request.method == 'GET':
        import random
        rand = random.randrange(0, Top100Songs.query.count())
        song = Top100Songs.query.all()[rand]
        session['songID'] = rand
    else:
        song = Top100Songs.query.all()[session['songID']]

    if form.validate_on_submit():
        if form.vote.data == 'yes':
            song.YesVotes += 1
            newyespct = song.YesVotes / float(song.NoVotes+song.YesVotes) * 100
            song.YesPercentage = newyespct
            db.session.commit()
            str1 = song.SongTitle
            str2 = song.Artist
            flash('Successfully voted YES for the song %s by %s' % (str1, str2))
        elif form.vote.data == 'no':
            song.NoVotes += 1
            newyespct = song.YesVotes / float(song.NoVotes+song.YesVotes) * 100
            song.YesPercentage = newyespct
            db.session.commit()
            str1 = song.SongTitle
            str2 = song.Artist
            flash('Successfully voted NO for the song %s by %s' % (str1, str2))
        elif form.vote.data == 'anachronism':
            song.AnachronismVotes += 1
            str1 = song.SongTitle
            str2 = song.Artist
            str3 = song.NominatedBy
            if song.AnachronismVotes >= 5:
                print '%s by %s submitted by %s might be from the wrong time frame' % (str1, str2, str3)
            db.session.commit()

flash('Successfully voted ANACHRONISM for the song %s by %s' % (str1, str2))
    else:
        flash('Something is fucked up.')
        
        return render_template('confirmation.html')
    
    
    return render_template('vote.html', song=song, form=form)