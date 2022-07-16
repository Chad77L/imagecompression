from flask import render_template, url_for,request,send_from_directory
from app import app
from app.forms import LoginForm
import os
from app import kmeanscompression
from app import dwtCompression
from app import fftCompression
from app import svdCompression
UPLOAD_FOLDER = os.path.join('static','upload')


app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route('/index')
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', user=user, posts=posts)


from flask import flash, redirect

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

@app.route('/')
@app.route('/imagecompression')
def imagecompression():
    return render_template('image_index.html')


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method== 'GET':
        return redirect(url_for('/'))
   if request.method == 'POST':
      
      f = request.files['file']
      if    f.filename =='' or f.filename[-4:]!='.png':
            return render_template('image_index.html',error="There is no image or image extension is not valid! (only .png image)")
      f.save(os.path.join('app','static','upload','org_img.png'))

      import cv2
      temp=cv2.imread(os.path.join('app','static','upload','org_img.png'),0)
      cv2.imwrite(os.path.join('app','static','upload','org_img.png'),temp)
      org_img_size= temp.shape
      size_on_disk= int(os.path.getsize(os.path.join('app','static','upload','org_img.png'))/1024)

      temp= cv2.imread(os.path.join('app','static','upload','org_img.png'),0)

      thuattoan1= kmeanscompression.KMeansCompressor(os.path.join('app','static','upload','org_img.png'))
      thuattoan2= dwtCompression.dwtCompression(os.path.join('app','static','upload','org_img.png'))
      thuattoan3= fftCompression.fftCompression(os.path.join('app','static','upload','org_img.png'))
      thuattoan4= svdCompression.svdCompression(os.path.join('app','static','upload','org_img.png'))


      from sklearn.metrics import mean_squared_error
      from math import sqrt

      rms1 = sqrt(mean_squared_error(temp, thuattoan1))
      rms2 = sqrt(mean_squared_error(temp, thuattoan2))
      rms3 = sqrt(mean_squared_error(temp, thuattoan3))
      rms4 = sqrt(mean_squared_error(temp, thuattoan4))


      cv2.imwrite(os.path.join('app','static','upload','thuattoan1.png'),thuattoan1)
      cv2.imwrite(os.path.join('app','static','upload','thuattoan2.png'),thuattoan2)
      cv2.imwrite(os.path.join('app','static','upload','thuattoan3.png'),thuattoan3)
      cv2.imwrite(os.path.join('app','static','upload','thuattoan4.png'),thuattoan4)
      
     
      thuattoan1_size= int(os.path.getsize(os.path.join('app','static','upload','thuattoan1.png'))/1024)
      thuattoan2_size= int(os.path.getsize(os.path.join('app','static','upload','thuattoan2.png'))/1024)
      thuattoan3_size= int(os.path.getsize(os.path.join('app','static','upload','thuattoan3.png'))/1024)
      thuattoan4_size= int(os.path.getsize(os.path.join('app','static','upload','thuattoan4.png'))/1024)

      return render_template('result.html', rms1=rms1,rms2=rms2,rms3=rms3,rms4=rms4,org_img_size=org_img_size,size_on_disk=size_on_disk, thuattoan1_size=thuattoan1_size,thuattoan2_size=thuattoan2_size,thuattoan3_size=thuattoan3_size,thuattoan4_size=thuattoan4_size)


@app.route('/upload/<filename>')
def upload(filename):
    return send_from_directory(app.config["UPLOAD_FOLDER"], filename)