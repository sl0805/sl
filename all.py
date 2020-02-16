from flask import Flask, render_template, request, redirect, url_for, session
import config
from flask_paginate import Pagination, get_page_parameter
from flask import Blueprint
from models import User, Video, Comment, Collect
from exts import db
from decorators import login_required
from sqlalchemy import or_
import pymysql

pymysql.install_as_MySQLdb()




app = Flask(__name__)

app.config.from_object(config)
db.init_app(app)




@app.route('/')
def index():
    page = int(request.args.get('page',1))
    per_page = int(request.args.get('per_page',2))
    paginate = Video.query.order_by(db.desc(Video.create_time)).paginate(page,per_page,error_out=False)
    videos = paginate.items
    user_id = session.get('user_id')
    user = User.query.filter(User.id==user_id).first()
    user_role = 'pup'
    if user:
        user_role = user.role
    return render_template('index.html',paginate=paginate,videos=videos,user_role=user_role)

@app.route('/tip_study/')
def tip_study():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    video_tip = '学习'
    videos = Video.query.filter(Video.tip == video_tip)
    if user_id:
        user_role = user.role
        return render_template('tip_study.html',videos = videos,user_role=user_role)
    user_role = 'pup'
    return render_template('tip_study.html',videos = videos,user_role=user_role)


@app.route('/tip_game/')
def tip_game():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    video_tip = '游戏'
    videos = Video.query.filter(Video.tip == video_tip)
    if user_id:
        user_role = user.role
        return render_template('tip_game.html',videos = videos,user_role=user_role)
    user_role = 'pup'
    return render_template('tip_game.html',videos = videos,user_role=user_role)



@app.route('/tip_star/')
def tip_star():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    video_tip = '明星'
    videos = Video.query.filter(Video.tip == video_tip)
    if user_id:
        user_role = user.role
        return render_template('tip_star.html',videos = videos,user_role=user_role)
    user_role = 'pup'
    return render_template('tip_star.html',videos = videos,user_role=user_role)


@app.route('/tip_pet/')
def tip_pet():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    video_tip = '萌宠'
    videos = Video.query.filter(Video.tip == video_tip)
    if user_id:
        user_role = user.role
        return render_template('tip_pet.html',videos = videos,user_role=user_role)
    user_role = 'pup'
    return render_template('tip_pet.html',videos = videos,user_role=user_role)


@app.route('/tip_anime/')
def tip_anime():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    video_tip = '动漫'
    videos = Video.query.filter(Video.tip == video_tip)
    if user_id:
        user_role = user.role
        return render_template('tip_anime.html',videos = videos,user_role=user_role)
    user_role = 'pup'
    return render_template('tip_anime.html',videos = videos,user_role=user_role)


@app.route('/tip_fun/')
def tip_fun():
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    video_tip = '鬼畜'
    videos = Video.query.filter(Video.tip == video_tip)
    if user_id:
        user_role = user.role
        return render_template('tip_fun.html',videos = videos,user_role=user_role)
    user_role = 'pup'
    return render_template('tip_fun.html',videos = videos,user_role=user_role)


@app.route('/detail/<video_id>/')
def detail(video_id):
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()
    user_role = 'pup'
    if user:
        user_role = user.role
    page = int(request.args.get('page',1))
    per_page = int(request.args.get('per_page',2))
    video = Video.query.filter(Video.id == video_id).first()
    paginate = Comment.query.filter(Comment.video_id==video_id).order_by(db.desc(Comment.create_time)).paginate(page,per_page,error_out=False)
    comments = paginate.items
    return render_template('detail.html', video=video,paginate=paginate,user_role=user_role, comments=comments)


@app.route('/add_comment/',methods=['POST','GET'])
@login_required
def add_comment():
    content = request.form.get('comment_content')
    video_id = request.form.get('video_id')
    comment = Comment(content=content)
    user_id = session['user_id']
    user = User.query.filter(User.id==user_id).first()
    comment.author = user
    video = Video.query.filter(Video.id == video_id).first()
    comment.video = video
    db.session.add(comment)
    db.session.commit()
    return redirect(url_for('detail', video_id=video_id))


@app.route('/login/', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        telephone = request.form.get('telephone')
        password = request.form.get('password')
        user = User.query.filter(User.telephone==telephone,User.password==password).first()
        if user:
            session['user_id'] = user.id
            session.permanent = True
            return redirect(url_for('index'))
        else:
            return '手机号码或密码错误，请核对后再登录'


@app.route('/logout/')
def logout():
    session.clear()
    return redirect(url_for('login'))


@app.route('/regist/', methods=['POST','GET'])
def regist():
    if request.method == 'GET':
        return render_template('regist.html')
    else:
        telephone = request.form.get('telephone')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.telephone==telephone).first()
        if user:
            return '该手机号码已被注册！'
        else:
            if password1 != password2:
                return '两次密码不一致'
            else:
                role = 'pup'
                avatar = 'origin.png'
                user = User(telephone=telephone, username=username,password=password1,avatar=avatar,role=role)
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))


@app.route('/change_pwd/', methods=['GET','POST'])
@login_required
def change_pwd():
    if request.method == 'GET':
        return render_template('change_pwd.html')
    else:
        password = request.form.get('password')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        user = User.query.filter(User.password==password).first()
        if user:
            if password1 == password2:
                user.password = password1
                db.session.commit()
                return redirect(url_for('logout'))
            else:
                return '两次密码不一致'
        else:
            return '原密码错误！'



@app.route('/person/')
def person():
    return render_template('person.html')

@app.route('/showtime/<author_id>/<author>/')
def showtime(author,author_id):
    author = User.query.filter(User.id==author_id).first()
    videos = Video.query.filter(Video.author_id==author_id).order_by(db.desc(Video.create_time))
    return render_template('showtime.html',author=author,videos=videos)


@app.route('/all_imformation/')
def all_imformation():
    users = User.query.order_by(User.id).all()
    id = session.get('user_id')
    return render_template('all_imformation.html',users=users,id=id)


@app.route('/person/userface/',methods=['GET','POST'])
def userface():
    if request.method == 'GET':
        return render_template('avatar.html')
    else:
        file = request.files['avatar_upload']
        path = "C:\\Users\\1\\Desktop\\python\\sl\\static\\images\\"
        file.save(path+file.filename)
        filename = file.filename
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        user.avatar = filename
        db.session.commit()
        return redirect(url_for('imformation'))


@app.route('/post_vedio/', methods=['GET','POST'])
@login_required
def post_vedio():
    if request.method == 'GET':
        return render_template('post_vedio.html')
    else:
        title = request.form.get('title')
        file = request.files['video_upload']
        path = "C:\\Users\\1\\Desktop\\python\\sl\\static\\video\\"
        file.save(path+file.filename)
        video_filename = file.filename
        file = request.files['pic_upload']
        path = "C:\\Users\\1\\Desktop\\python\\sl\\static\\images\\"
        file.save(path+file.filename)
        pic_filename = file.filename
        tip = request.values.get('num')
        thumb_num = 0
        collect_num = 0
        video = Video(title=title,pic_filename=pic_filename,video_filename=video_filename,tip=tip,thumb_num=thumb_num,collect_num=collect_num)
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        video.author = user
        db.session.add(video)
        db.session.commit()
        return redirect(url_for('imformation'))


@app.route('/search/')
def search():
    keyword = request.args.get('keyword')
    # title/content里面查找
    page = int(request.args.get('page',1))
    per_page = int(request.args.get('per_page',20))
    paginate = Video.query.filter(or_(Video.title.contains(keyword),User.username.contains(keyword))).order_by(db.desc(Video.create_time)).paginate(page,per_page,error_out=False)
    videos = paginate.items
    return render_template('index.html',paginate=paginate,videos=videos)
    # return redirect(url_for('index',videos=videos))


@app.route('/my_video/')
def my_video():
    context = {
        'videos': Video.query.order_by(db.desc(Video.create_time)).all()
    }
    return render_template('my_video.html',**context)


@app.route('/delete/',methods=['POST'])
def delete():
    video_id = request.form.get('video_id')
    video = Video.query.filter(Video.id == video_id).first()
    db.session.delete(video)
    db.session.commit()
    return redirect(url_for('my_video'))


@app.route('/delete_comment/<video_id>/',methods=['POST'])
def delete_comment(video_id):
    comment_id = request.form.get('comment_id')
    comment = Comment.query.filter(Comment.id == comment_id).first()
    db.session.delete(comment)
    db.session.commit()
    return redirect(url_for('detail',video_id = video_id))


@app.route('/delete_user/',methods=['POST'])
def delete_user():
    user_id = request.form.get('user_id')
    user = User.query.filter(User.id==user_id).first()
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('all_imformation'))


@app.route('/my_collect/')
def my_collect():
    user_id = session.get('user_id')
    context = {
        'collects': Collect.query.filter(Collect.author_id == user_id).all()
    }
    # collects = Collect.query.filter(Collect.author_id == user_id)
    return render_template('my_collect.html',**context)


@app.route('/collect/',methods=['POST'])
@login_required
def collect():
    # 把收藏数加一，知道点赞人的ID，知道视频的ID
    video_id = request.form.get('video_id')
    user_id = session.get('user_id')
    user = User.query.filter(User.id==user_id).first()
    video = Video.query.filter(Video.id == video_id).first()
    collect = Collect(video_id=video_id,author_id=user_id)
    collect.author = user
    collect.video = video
    db.session.add(collect)
    db.session.commit()
    video = Video.query.filter(Video.id == video_id).first()
    video.collect_num = video.collect_num + 1
    db.session.commit()
    return redirect(url_for('detail', video_id=video_id))


@app.route('/thumb/',methods=['POST'])
@login_required
def thumb():
    video_id = request.form.get('video_id')
    video = Video.query.filter(Video.id == video_id).first()
    video.thumb_num = video.thumb_num + 1
    db.session.commit()
    return redirect(url_for('detail', video_id=video_id))


@app.route('/imformation/',methods=['POST','GET'])
def imformation():
    return render_template('imformation.html')


@app.context_processor
def my_context_processor():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.filter(User.id == user_id).first()
        if user:
            return{'user':user}
    return {}


if __name__ == '__main__':
    app.run()