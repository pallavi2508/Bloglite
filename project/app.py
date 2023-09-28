from flask import Flask,render_template,request,url_for,redirect,request
from flask_sqlalchemy import SQLAlchemy
from models import *
import base64 

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bloglite.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=True
db.init_app(app)
app.app_context().push()


def num_followers(self):
    return(self.followers.count())

    
def num_following(self):
    return(self.following.count())

@app.route("/",methods = ['GET','POST'])
def login():
    if request.method=="GET":
        return render_template("login.html")
    if request.method=="POST":
        users = User.query.all()
        username = request.form["username"]
        password = request.form["pwd"]

        for user in users:
            if username == user.username and password == user.password:
                print("Logged in successfully")
                cuser = User.query.filter(User.username == username).one()
                uid = cuser.user_id
                return redirect(url_for("feed", uid=uid))
               

@app.route("/register",methods=['GET','POST'])
def register():
    if request.method == "GET":
        return render_template ("register.html")

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["pwd"]
        cpassword = request.form["cpassword"]
        if password == cpassword:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for("login"))

@app.route("/post/create/<int:uid>", methods = ['GET', 'POST'])
def add_post(uid):
    if request.method=="GET":
        post = Post.query.filter(Post.up_id == uid)
        cuser = User.query.filter(User.user_id == uid).one()
        uname = cuser.username
        return render_template("add_post.html", uid=uid, uname=uname, picture=post)
    if request.method=="POST":
        caption=request.form["caption"]
        pic=request.files['post_pic']
        new_post=Post(up_id=uid,title=caption,picture=pic.read())
        db.session.add(new_post)
        db.session.commit()
        return redirect(url_for("feed",uid=uid))

@app.route("/post/update/<int:uid>/<int:up_id>", methods = ['GET', 'POST'])
def update_post(uid,up_id):
    if request.method=="GET":
        post = Post.query.filter(Post.up_id == up_id)
        cuser = User.query.filter(User.user_id == uid).one()
        fuser = User.query.filter(User.user_id == uid).one()
        uname = cuser.username
        return render_template("update_post.html", uid=uid, uname=uname, picture=post ,up_id=up_id,fuser=fuser)
    if request.method=="POST":
        post = Post.query.filter(Post.up_id == up_id).one()
        post.title=request.form["caption"]
        fuser = User.query.filter(User.user_id == uid).one()
        cuser = User.query.filter(User.user_id == uid).one()
        post.picture=(request.files['post_pic']).read()
        db.session.commit()
        return redirect(url_for('user',uid=uid,fid=uid))

@app.route("/delete_post/<int:uid>/<int:fid>/<int:id>", methods=["GET", "POST"])
def delete_post(id, uid ,fid):
    cuser = User.query.filter(User.user_id == uid).one()
    fuser = User.query.filter(User.user_id == fid).one()
    post = Post.query.filter(Post.id==id).one()
    if not post:
        return redirect(url_for('user',uid=uid,fid=fid))
    if fuser != cuser:
        return redirect(url_for('user',uid=uid,fid=fid))
    db.session.delete(post)
    db.session.commit()
    return redirect(url_for('user',uid=uid,fid=fid))
    

@app.route("/pfp/set/<int:uid>/<int:fid>", methods = ['GET', 'POST'])
def add_pfp(uid, fid):
    if request.method=="GET":
        return render_template("add_pfp.html", uid=uid,fid=fid)
    if request.method=="POST":
        cuser = User.query.filter(User.user_id == uid).one()
        fuser = User.query.filter(User.user_id == fid).one()
        cuser.bio=request.form["bio"]
        db.session.commit()
        return redirect(url_for('user',uid=uid,fid=fid))

@app.route("/feed/<int:uid>",methods=["GET","POST"])
def feed(uid):
    if request.method=="GET":
        user=User.query.filter(User.user_id==uid)
        fuser = User.query.filter(User.user_id == uid).one()
        posts=Post.query.all()
        postnlist=[]
        for post in posts:
            plist={}
            plist["post_user"] = User.query.get(post.up_id)
            plist["post"]=post
            img=base64.b64encode(post.picture).decode('utf-8')
            plist['image']=img
            postnlist.append(plist)

        
        cuser = User.query.filter(User.user_id == uid).one()
        uname = cuser.username
        return render_template("feed1.html", uid=uid, uname=uname,postnlist=postnlist,user=user,cuser=cuser,fuser=fuser)

@app.route("/user/<int:uid>/<int:fid>",methods=["GET","POST"])
def user(uid,fid):
    if request.method=="GET":
        if fid==uid:
            user = User.query.get(fid)
            fuser = User.query.filter(User.user_id == fid).one()
            posts=Post.query.filter(Post.up_id==fid)
            postnlist=[]
            for post in posts:
                plist={}
                plist["post_user"] = User.query.get(post.up_id)
                plist["post"]=post
                img=base64.b64encode(post.picture).decode('utf-8')
                plist['image']=img
                postnlist.append(plist)

            cuser = User.query.filter(User.user_id == uid).one()
            uname = cuser.username
        
            return render_template('current_user.html', user=user, posts=posts, followers=followers, following=following,uid=uid,postnlist=postnlist,fid=fid,cuser=cuser,fuser=fuser)


        if fid!=uid:
            user = User.query.get(fid)
            fuser = User.query.filter(User.user_id == fid).one()
            posts=Post.query.filter(Post.up_id==fid)
            postnlist=[]
            for post in posts:
                plist={}
                plist["post_user"] = User.query.get(post.up_id)
                plist["post"]=post
                img=base64.b64encode(post.picture).decode('utf-8')
                plist['image']=img
                postnlist.append(plist)

            cuser = User.query.filter(User.user_id == uid).one()
            uname = cuser.username
        
            return render_template('user.html', user=user, posts=posts, followers=followers, following=following,uid=uid,postnlist=postnlist,fid=fid,cuser=cuser,fuser=fuser)

            

        

@app.route("/user/following/<int:uid>/<int:fid>",methods=["GET","POST"])
def following(uid,fid):
    if request.method=="GET":
        cuser = User.query.filter(User.user_id == uid).one()
        fuser = User.query.filter(User.user_id == fid).one()
        followers=Followers.query.filter_by(follower_id=fid).all()
        followerslist=[]
        for user in followers:
            followerslist.append(User.query.get(user.following_id))
        followingcount=len(followerslist)
        return render_template("following.html",uid=uid,fid=fid,followerslist=followerslist,cuser=cuser,fuser=fuser,followingcount=followingcount)

@app.route("/user/followers/<int:uid>/<int:fid>",methods=["GET","POST"])
def followers(uid,fid):
    if request.method=="GET":
        cuser = User.query.filter(User.user_id == uid).one()
        fuser = User.query.filter(User.user_id == fid).one()
        followings=Followers.query.filter_by(following_id=fid).all()
        followingslist=[]
        for user in followings:
            followingslist.append(User.query.get(user.follower_id))
        followerscount=len(followingslist)
        return render_template("followers.html",uid=uid,fid=fid,cuser=cuser,followingslist=followingslist,fuser=fuser,followerscount=followerscount)


@app.route("/search/<int:uid>",methods=["GET","POST"])
def search(uid):
    if request.method=="GET":
        queryname=request.args.get("queryname")
        resultsname=search_users(queryname)
        cuser = User.query.filter(User.user_id == uid).one()
        for users in resultsname:
            fid = users.user_id
            fuser = User.query.filter(User.user_id == fid).one()
        return render_template("search.html",queryname=queryname,resultsname=resultsname,uid=uid,cuser=cuser)
    
def search_users(queryname):
    
    users=User.query.filter(User.username==queryname).all()
    return users



@app.route('/user/<int:uid>/follow/<int:fid>',methods=['POST','GET'])
def followuser(uid, fid):
        cuser = User.query.filter(User.user_id == uid).one()
        fuser = User.query.filter(User.user_id == fid).one()
        if fuser != cuser:
            new_follow = Followers(follower_id=uid, following_id=fid)
            db.session.add(new_follow)
            db.session.commit()

            return redirect(url_for('user',uid=uid,fid=fid))

        else:
            return('You cannot follow yourself')


@app.route('/user/<int:uid>/unfollow/<int:fid>', methods=['POST','GET','DELETE'])
def unfollow(uid,fid):
        cuser = User.query.filter(User.user_id == uid).one()
        fuser = User.query.filter(User.user_id == fid).one()
        
        if fuser != cuser:
            unf = Followers.query.filter(Followers.follower_id==uid, Followers.following_id==fid).one()
            db.session.delete(unf)
            db.session.commit()
            return redirect(url_for('user',uid=uid,fid=fid))
        else:
            return('You cannot unfollow yourself')

        
        

@app.route('/logout')
def logout():
    db.session.close()
    return redirect(url_for('login'))


if __name__ == '__main__':
  # Run the Flask app
  app.run(host='0.0.0.0',debug=True)



