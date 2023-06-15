import datetime
from flask import Flask,render_template, redirect, url_for, flash, request, abort
from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc

from flask import current_app as app
from twitterProject.forms import Signup, Login, ResetRequest, UpdateProfile
from twitterProject.models import  UserManagement, db
from twitterProject.forms import Signup, Login, UpdateProfile, createTweet
from twitterProject.utils import save_bg_picture, save_profile_picture, delete_old_images, save_tweet_picture

import datetime

@app.route('/', methods=['POST', 'GET'])
@app.route('/home',methods=['POST', 'GET'])
def home():
    register_form = Signup()
    login_form = Login()

    if register_form.validate_on_submit() and register_form.submit.data:
        if register_form.password.data != register_form.confirm_password.data:
            flash("PLease enter valid Password", 'error')

        hashed_password = generate_password_hash(register_form.password.data, method='sha256')
        new_user = UserManagement(username=register_form.username.data, email=register_form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return render_template('sign.html')

    if login_form.validate_on_submit():
        user_info = UserManagement.query.filter_by(username=login_form.username.data).first()
        if user_info:
            if check_password_hash(user_info.password, login_form.password.data):
                login_user(user_info, remember=login_form.remember.data)
                return redirect(url_for('dashboard'))
            else:
                return render_template('errorP.html')
        else:
            return render_template('errorU.html')

    return render_template('start.html', register_form=register_form, login_form=login_form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route('/account')
@login_required
def account():
    update = UpdateProfile()

    page = request.args.get('page',1,type=int)
    all_posts = Post.query\
        .filter_by(user_id=current_user.id)\
        .order_by(desc(Post.id))\
        .paginate(page=page,per_page=5)
    retweets = Retweet.query\
        .filter_by(user_id=current_user.id)\
        .order_by(desc(Retweet.id))

    return render_template('account.html',profile=profile_pic,background=bg_pic,update=update,timeline=all_posts, retweets=retweets)



@app.route('/reset_password', methods=['GET','POST'])
def reset_password():
    """
    Add reset feature
    """
    breakpoint()
    form_reset = ResetRequest()
    if form_reset.validate_on_submit():
        user_info = UserManagement.query.filter_by(email=form_reset.email.data).first()
        if user_info:
            flash("Reset request sent to your email address.!!!!", 'success')
            return redirect(url_for('home'))
    return render_template('reset_password.html', form=form_reset)

@app.route('/reset_password/<token>', methods= ["GET", "POST"])
def reset_token(token):
    """
    Reset Password using Token 
    """
    user = UserManagement.verified_token(token=token)
    if user is None:
        flash("PLease try agin you might be expire")
        return redirect(url_for('reset_password'))

    form = ResetRequest()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        user.password = hashed_password
        db.session.commit()
        flash('Password change Successfully', 'success')
        return redirect(url_for('home'))
    return  render_template('change_password.html', title='Change Password', form=form)



@app.route('/dashboard',methods=['GET','POST'])
@login_required
def dashboard():
    user_tweet = createTweet()
    if user_tweet.validate_on_submit():

        x = datetime.datetime.now()
        currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))

        if user_tweet.tweet_img.data:
            tweet_img = save_tweet_picture(user_tweet.tweet_img.data)
            post = Post(tweet=user_tweet.tweet.data, stamp=currentTime, author=current_user, post_img=tweet_img)
        else:
            post = Post(tweet=user_tweet.tweet.data, stamp=currentTime, author=current_user)

        db.session.add(post)
        db.session.commit()

        to_timeline = Timeline(post_id=post.id)
        db.session.add(to_timeline)
        db.session.commit()

        flash('The Tweet was added to your timeline!','success')
        return redirect(url_for('dashboard'))

    page = request.args.get('page',1,type=int)
    timeline = Timeline.query\
        .order_by(desc(Timeline.id))\
        .paginate(page=page,per_page=5)
    return render_template('dashboard.html',name = current_user.username,tweet = user_tweet, timeline=timeline)

@app.route('/view_profile/<int:account_id>',methods=['GET','POST'])
@login_required
def viewProfile(account_id):
    if account_id == current_user.id:
        return redirect(url_for('account'))

    get_user = User_mgmt.query.filter_by(id=account_id).first()
    profile_pic = url_for('static',filename='Images/Users/profile_pics/' + get_user.image_file)
    bg_pic = url_for('static',filename='Images/Users/bg_pics/' + get_user.bg_file)

    page = request.args.get('page',1,type=int)
    all_posts = Post.query\
        .filter_by(user_id=get_user.id)\
        .order_by(desc(Post.id))\
        .paginate(page=page,per_page=5)
    retweets = Retweet.query\
        .filter_by(user_id=get_user.id)\
        .order_by(desc(Retweet.id))

    return render_template('view_profile.html',profile=profile_pic,background=bg_pic,timeline=all_posts,user=get_user,retweets=retweets)



@app.route('/bookmark/<int:post_id>',methods=['GET','POST'])
def save_post(post_id):
    saved_post = Bookmark(post_id=post_id,user_id=current_user.id)
    db.session.add(saved_post)
    db.session.commit()
    flash('Saved tweet to bookmark!','success')
    return redirect(url_for('dashboard'))


@app.route('/unsaved_posts/<int:post_id>',methods=['GET','POST'])
def unsave_post(post_id):
    removed_post = Bookmark.query\
        .filter_by(post_id=post_id)\
        .first()
    db.session.delete(removed_post)
    db.session.commit()
    flash('Post removed from bookmark!','success')
    return redirect(url_for('dashboard'))

@app.route('/saved_posts/')
def bookmarks():
    posts = Bookmark.query\
        .filter_by(user_id=current_user.id)\
        .order_by(desc(Bookmark.id))
    empty = False
    if posts == None:
        empty = True
    return render_template('bookmarks.html',posts=posts, empty=empty)





@app.route('/retweet/<int:post_id>',methods=['GET','POST'])
@login_required
def retweet(post_id):

    post = Post.query.get_or_404(post_id)
    new_tweet = createTweet()

    if new_tweet.validate_on_submit():

        x = datetime.datetime.now()
        currentTime = str(x.strftime("%d")) +" "+ str(x.strftime("%B")) +"'"+ str(x.strftime("%y")) + " "+ str(x.strftime("%I")) +":"+ str(x.strftime("%M")) +" "+ str(x.strftime("%p"))

        retweet = Retweet(tweet_id=post.id,user_id=current_user.id,retweet_stamp=currentTime,retweet_text=new_tweet.tweet.data)
        db.session.add(retweet)
        db.session.commit()

        to_timeline = Timeline(retweet_id=retweet.id)
        db.session.add(to_timeline)
        db.session.commit()

        msg = 'You retweeted @'+post.author.username+"'s tweet!"
        flash(msg,'success')
        return redirect(url_for('dashboard'))

    return render_template('retweet.html',post=post, tweet=new_tweet)

@app.route('/delete/<int:post_id>')
@login_required
def delete(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    return render_template('delete_post.html',post=post)

@app.route('/delete_retweet/<int:post_id>')
@login_required
def delete_retweet(post_id):
    retweet = Retweet.query.get_or_404(post_id)
    if retweet.retwitter != current_user:
        abort(403)
    return render_template('delete_post.html',retweet=retweet)

@app.route('/delete_post/<int:post_id>',methods=['POST'])
@login_required
def delete_tweet(post_id):

    post_bk = Bookmark.query.filter_by(post_id=post_id)
    if post_bk != None:
        for i in post_bk:
            db.session.delete(i)
            db.session.commit()

    remove_from_timeline = Timeline.query.filter_by(post_id=post_id).first()
    if remove_from_timeline.from_post.author != current_user:
        abort(403)
    db.session.delete(remove_from_timeline)
    db.session.commit()

    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()

    flash('Your tweet was deleted!','success')
    return redirect(url_for('dashboard'))

@app.route('/delete_retweeted_post/<int:post_id>',methods=['POST'])
@login_required
def delete_retweeted_tweet(post_id):

    post_bk = Bookmark.query.filter_by(post_id=post_id)
    if post_bk != None:
        for i in post_bk:
            db.session.delete(i)
            db.session.commit()

    remove_from_timeline = Timeline.query.filter_by(retweet_id=post_id).first()
    if remove_from_timeline.from_retweet.retwitter != current_user:
        abort(403)
    db.session.delete(remove_from_timeline)
    db.session.commit()

    retweet = Retweet.query.get_or_404(post_id)
    if retweet.retwitter != current_user:
        abort(403)
    db.session.delete(retweet)
    db.session.commit()

    flash('Your tweet was deleted!','success')
    return redirect(url_for('dashboard'))