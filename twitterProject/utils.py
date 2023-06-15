from twitterProject import create_app
import secrets
import os
from flask import url_for

def save_profile_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Images/Users/profile_pics', picture_fn)
    form_pic.save(picture_path)
    return picture_fn

def save_bg_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Images/Users/bg_pics', picture_fn)
    form_pic.save(picture_path)
    return picture_fn

def delete_old_images(image, bg_image):
    profile_pic_path = os.path.join(app.root_path, 'static/Images/Users/profile_pics', image)
    bg_pic_path = os.path.join(app.root_path, 'static/Images/Users/bg_pics', bg_image)
    if image!='default.jpg' and image!='':
        try:
            os.remove(profile_pic_path)
        except OSError:
            pass
    if bg_image!='default_bg.jpg' and bg_image!='':
        try:
            os.remove(bg_pic_path)
        except OSError:
            pass

def save_tweet_picture(form_pic):
    random_hex = secrets.token_hex(8)
    f_name,f_ext = os.path.splitext(form_pic.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/Images/Tweets', picture_fn)
    form_pic.save(picture_path)
    return picture_fn

from flask_mail import Message

def sent_email(user):
    token = user.get_token()
    msg = Message('Password Reset Request', recipients=[user.email], sender='noreply@gmail.com')
    msg.body = f''' To reset your password. Please follow below link 
    {url_for('reset_token', token=token, _external=True)}

    if you did not send it please ignore
    
    '''
    pass

