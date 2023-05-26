from flask import Flask , render_template , redirect , url_for , request
from flask_sqlalchemy import SQLAlchemy           

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:////Users/Üzeyir ÖĞÜR/Desktop/TodoApp/todo.db'                  #bizim todo.db nin yolunu belirttik kaydediceğimiz ortam
db = SQLAlchemy(app)                       #db sql işlemleri için lazım obje ürettik sonra bunu app formuna aktardık

#Biz sql sorguları yazarak tablo oluşturup veri ekleyip sildiğimiz bir yapı vardı
#ORM bu sorgularla uğraşmadan direkt class ve methodlarla bunları yapmamızı sağlayan bir yapıdır


#TABLO OLUŞTURMA CLASS I
class Todo(db.Model) :                   #ORM içindeki model yapısından tablo oluşturmak istediğimizi söyledik
    id = db.Column(db.Integer , primary_key = True)                    #db.Column = bir sütun oluştur demek // db.Integer = bir integer değer olucak demek // primary_key = otomatik ekledikçe bir artsın demek
    title = db.Column(db.String(80))                                #db.String(80) = string oluştur max 80 karakter olsun demek
    title2 = db.Column(db.String(90))
    complete = db.Column(db.Boolean)                                   #bunu oluşturma amacımız ise her işimizi tamamlamışsak true tamamlamaışsak false olsun demek


app.app_context().push()
db.create_all()                #oluşturmak için tabloyu 


@app.route("/")
def index() :
    todos = Todo.query.all()                                  #Todo.query.all() bize tablomuzdaki bütün her şeyi liste şeklinde sözlük biçiminde dönderiyor
    
    return render_template("index.html",todos = todos)

@app.route("/complete/<string:id>")
def Complete(id) :
    todo = Todo.query.filter_by(id = id).first()              #burada basılan id nin numarasını aldık ve todo değişkenine atadık
    """if todo.complete == True :
        todo.complete == False 
    else :
        todo.complete == True """

    todo.complete = not todo.complete               #bu işlem yukarıdaki if bloğu yerine daha kısa olduğu için mantıklı tersini al demek    
    db.session.commit()                             #her veritabanında değişiklik yaptığımızda şart 
    return redirect(url_for("index"))

@app.route("/delete/<string:id>")
def Delete(id) :
    todo =  Todo.query.filter_by(id = id).first()

    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))



@app.route("/add",methods = ["POST"])
def addTodo() :  
    title = request.form.get("title") 
    title2 = request.form.get("title2")                                     
    newTodo = Todo(title = title ,title2 = title2 , complete = False )
    db.session.add(newTodo)                              #veritabanına ekleme yöntemi
    db.session.commit() 

    return redirect(url_for("index"))


















if __name__ == "__main__" :
    app.run(debug = True)
   

