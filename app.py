import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("mongodb+srv://shilmapuspita:Shilma17!@cluster0.luuvj.mongodb.net/")
DB_NAME =  os.environ.get("dbsparta")

client = MongoClient('mongodb+srv://shilmapuspita:Shilma17!@cluster0.luuvj.mongodb.net/')

db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
   return render_template('index.html')

@app.route("/bucket", methods=["POST"])
def bucket_post():
    bucket_receive = request.form["bucket_give"] 
    count = db.bucket.count_documents({})
    num = count + 1 #menyambungkan setiap dokumen baru
    doc = {
        'num':num,
        'bucket': bucket_receive,
        'done':0 #0 menandakan belum selesai, jika 1 berarti sdh selesai
    }
    db.bucket.insert_one(doc)
    return jsonify({'msg':'data saved!'})

@app.route("/bucket/done", methods=["POST"])
def bucket_done():
    num_receive = request.form["num_give"] #yg menentukan client yg memberikan data dgn nama num_give
    db.bucket.update_one(
        {'num': int(num_receive)}, #int untuk mencegah user memasukan data type string
        {'$set': {'done': 1}}
    )
    return jsonify({'msg': 'Update done!'})

@app.route("/bucket", methods=["GET"])
def bucket_get():
    buckets_list = list(db.bucket.find({},{'_id':False}))
    return jsonify({'buckets':buckets_list})

@app.route('/delete', methods=['POST'])
def delete_bucket():
    data = request.get_json()  # terima data dalam format JSON
    num_receive = data['num_give']  # mengambil nilai num dari request

    # menghapus item dari database berdasarkan num
    db.bucket.delete_one({'num': int(num_receive)})
    
    return jsonify({'msg': 'Bucket list item di delete!'})

if __name__ == '__main__':
   app.run('0.0.0.0', port=5000, debug=True)