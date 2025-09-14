from flask import Flask, render_template, flash, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import InputRequired
from werkzeug.utils import secure_filename
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecretkey'

# Upload folder inside static
app.config['UPLOAD_FOLDER'] = os.path.join(app.root_path, 'static', 'files')
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)  # Create folder if it doesn't exist

# Flask-WTF form
class UploadFileForm(FlaskForm):
    file = FileField("Choose a file", validators=[InputRequired()])
    submit = SubmitField("Upload")

@app.route('/', methods=['GET', 'POST'])
def home():
    form = UploadFileForm()
    if form.validate_on_submit():
        file = form.file.data
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash(f'File "{filename}" uploaded successfully!')
        return redirect(url_for('home'))
    
    # List files in the upload folder
    uploaded_files = os.listdir(app.config['UPLOAD_FOLDER'])
    return render_template('index.html', form=form, uploaded_files=uploaded_files)

if __name__ == '__main__':
    app.run(debug=True)