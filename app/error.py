from flask import flash

def catch(e):
    if e == 1062:
        flash("Ese nombre no puede ser usado ya que ya ha sido registrado anteriormente.")
    else:
        flash("Un error desconocido no permitió guardar tu código QR de manera correcta.")
