from flask import Flask, render_template, request

import os

app = Flask(__name__)

# 저장소 설정
app.config["UPLOAD_FOLDER"] = "uploads"

os.makedirs(app.config["UPLOAD_FOLDER"], exist_ok=True)


def allowerd_file(filename):
    ALLOWERD_EXT = {"png", "jpg", "jpeg", "gif"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWERD_EXT


@app.route("/")
def index():
    return render_template("form.html")


@app.route("/login", metthods=["POST"])
def login():
    id = request.form.get("id")
    pw = request.form.get("pw")
    print(f"입력한 ID는 {id}, PW는 {pw}")
    # if id == u['id'] and pw == u['pw']:

    return render_template("login.html", name=id)


@app.route("upload", methods=["POST"])
def upload_file():
    file = request.files["photo"]
    print(file)

    filename = file.filename  # 우리의 실습상 사용자가 올린 파일명을 그대로 사용하지만,
    # 실서비스라면 여러 사용자들의 업로드한 파일이 겹쳐서 overwrite 될 수 있음으로, 파일명을 적절하게 바뀐다. (예, timestamp,hash,userid, 등등 prefix)
    # filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    # file.save(filepath)
    # return "파일 잘 받았음"

    if file and allowerd_file(file.filename):
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
        file.save(filepath)
        return "파일 잘 받았음"
    else:
        return f"지원되지 않는 파일 입니다. 파일명: {file.filename}"


if __name__ == "__main__":
    app.run(debug=True)
