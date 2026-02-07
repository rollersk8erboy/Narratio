import pyqrcode
from flask import Blueprint, current_app, render_template, request, redirect, url_for, flash
from pathlib import Path
from gtts import gTTS
from app import database
from app import error
from app.constants import ALL, ONE, VALUE

codes = Blueprint('codes', __name__)

@codes.route("/", defaults={'q': '', 'p': 1}, methods=['GET', 'POST'])
@codes.route("/search/<q>", defaults={'p': 1}, methods=['GET', 'POST'])
@codes.route("/page/<int:p>", defaults={'q': ''}, methods=['GET', 'POST'])
@codes.route("/search/<q>/page/<int:p>", methods=['GET', 'POST']) 
def index(q, p):
    if request.method == 'POST':
        q = request.form.get('q', '')
        return redirect(url_for('codes.index', q=q, p=1))
    codes = database.execute("CALL get_codes_with_pagination(%s, %s)", ALL, [q, p])
    return render_template("codes/index.html", codes=codes, q=q, p=p)

@codes.route("/create")
def create():
    return render_template("codes/create.html")

@codes.route("/store", methods=["POST"])
def store():
    mycodename = request.form.get('mycodename', '')
    mydescription = request.form.get('mydescription', '')
    myfiletype = request.form.get('myfiletype', '')
    mylanguage = request.form.get('mylanguage', '')
    myaudio = request.files.get('myaudio')
    try:
        mycodeid = database.execute("CALL create_new_code(%s, %s, %s, %s)", VALUE, [mycodename, mydescription, myfiletype, mylanguage], 'codeid')
        qr_path = Path(current_app.static_folder) / 'svg.nosync' / f'{mycodeid}.svg'
        qr_path.parent.mkdir(parents=True, exist_ok=True)
        pyqrcode.create(str(mycodeid)).svg(str(qr_path), scale=8)
        audio_path = Path(current_app.static_folder) / 'mp3.nosync' / f'{mycodeid}.mp3'
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        if myfiletype == 'mp3' and myaudio:
            myaudio.save(str(audio_path))
        elif myfiletype == 'txt' and mydescription:
            gTTS(text=mydescription, lang=mylanguage).save(str(audio_path))
        flash("Tu código QR se guardó de manera correcta.")
        return redirect(url_for('codes.index'))
    except Exception as e:
        error.catch(getattr(e, 'errno', None))
        return redirect(url_for('codes.create'))

@codes.route('/edit/<int:mycodeid>', methods=["GET"])
def edit(mycodeid):
    code = database.execute("CALL get_a_code(%s)", ONE, [mycodeid])
    if code is None:
        flash("El código QR al que intentas acceder no existe.")
        return redirect(url_for('codes.index'))
    return render_template("codes/edit.html", code=code)
    
@codes.route('/update/<int:mycodeid>', methods=["POST"])
def update(mycodeid):
    mycodename = request.form.get('mycodename', '')
    mydescription = request.form.get('mydescription', '')
    myfiletype = request.form.get('myfiletype', '')
    mylanguage = request.form.get('mylanguage', '')
    myaudio = request.files.get('myaudio')
    try:
        mycodeid = database.execute("CALL update_code(%s, %s, %s, %s, %s)", VALUE, [mycodeid, mycodename, mydescription, myfiletype, mylanguage], 'codeid')
        audio_path = Path(current_app.static_folder) / 'mp3.nosync' / f'{mycodeid}.mp3'
        audio_path.parent.mkdir(parents=True, exist_ok=True)
        if myfiletype == 'mp3' and myaudio:
            myaudio.save(str(audio_path))
        elif myfiletype == 'txt' and mydescription:
            gTTS(text=mydescription, lang=mylanguage).save(str(audio_path))
        flash("Tu código QR se actualizó de manera correcta.")
        return redirect(url_for('codes.index'))
    except Exception as e:
        error.catch(getattr(e, 'errno', None))
        return redirect(url_for('codes.edit', mycodeid=mycodeid))


@codes.route('/destroy/<int:mycodeid>', methods=["POST"])
def destroy(mycodeid):
    try:
        database.execute("CALL destroy_qrcode(%s)", VALUE, [mycodeid], 'codeid')
        (Path(current_app.static_folder) / 'svg.nosync' / f'{mycodeid}.svg').unlink(missing_ok=True)
        (Path(current_app.static_folder) / 'mp3.nosync' / f'{mycodeid}.mp3').unlink(missing_ok=True)
        flash("Tu código QR se eliminó de manera correcta.")
    except Exception as e:
        error.catch(getattr(e, 'errno', None))
    return redirect(url_for('codes.index'))

@codes.route('/show/<int:mycodeid>', methods=["GET"])
def show(mycodeid):
    code = database.execute("CALL get_a_code(%s)", ONE, [mycodeid])
    if code is None:
        flash("El código QR al que intentas acceder no existe.")
        return redirect(url_for('codes.index'))
    return render_template("codes/show.html", code=code)


        