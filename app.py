# Team Robert’); DROP TABLE S\*;-- (a.k.a little_bobby_tables)
#       Amanda Chen (PM), Jesse Hall, Kiran Vuksanaj, Tanzim Elahi
# SoftDev1 Pd1
# P00 -- Da Art of Storytellin' (Part X)
# 2019-10-17


from flask import Flask, render_template, request, redirect, url_for
app = Flask(__name__)


name = "Storybuilder"
roster = "little_bobby_tables"

@app.route("/")
def root():
    print(app)
    return render_template('root.html',
                            team = name,
                            rost = roster)

@app.route("/auth")
def authenticate():
    return render_template('out.html',
                            team = name,
                            rost = roster,
                            arg_user = str(request.args["username"]),
                            arg_method = str(request.method))


@app.route("/error")
def err():
    return "blaaa"


if __name__ == "__main__":
    app.debug = True
    app.run()
