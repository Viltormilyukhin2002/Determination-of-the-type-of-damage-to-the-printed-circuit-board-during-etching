from flask import Flask, render_template, flash
from werkzeug.utils import secure_filename, redirect
from forms import UploadForm
from inference_onnx import *
from save import new_filename, unpuck
from flask_sqlalchemy import SQLAlchemy
from database import Item


app = Flask(__name__)
app.config.from_object(os.environ.get('FLASK_ENV') or 'config.DevelopementConfig')
db = SQLAlchemy(app)


@app.route('/')
def upload_form():
    return render_template("upload.html", form=UploadForm(), data=Item.query.all())


@app.route('/', methods=['POST'])
def upload_file():
    form = UploadForm()
    if form.validate_on_submit():
        images = form.photo.data
        lenght = len(images)
        for i in images:
            if str('.'.join(i.filename.split('.')[1:])) == 'zip':
                lenght += (unpuck(i) - 1)
            else:
                i.filename = new_filename(i.filename)
                i.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(str(i.filename))))
        result = script(lenght)
        for k, v in result:
            predicted_class = np.argmax(v)

            item = Item(cad=str(k.replace('Image', 'Cad')), image=str(k), res=str(CLASSES[predicted_class]),
                        probability=str(v.flatten()[predicted_class]))
            db.session.add(item)
            db.session.commit()
        if len(images) % 2 == 0:
            flash('File(s) successfully uploaded', category='success')
        else:
            flash('Some of the images you sent didn\'t have a pair', category='warning')
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)
