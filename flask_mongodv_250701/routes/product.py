
from flask import request, jsonify
from pymongo import MongoClient  # 몽고클라이언트라는 함수 가져오겠다
from bson import ObjectId    # 바이너리 json

client = MongoClient("mongodb://localhost:27017/") #스프링부트에서 application properties에 넣은것 처럼
db = client["shopdb"]
products = db["products"]

#함수만들기
def convert_doc(doc):
    doc["id"]= str(doc["_id"]) #_id를 id로 바꾸기 위해
    del doc["_id"]
    return doc

#루트 경로
def root_path():
    return "파이썬 플라스크 루트"

#post, get 등은 app.py에서 구분할 것임
#insert
def create_product(): #매개변수가 없는 이유 body로 보냈기 때문
    #클라이언트에서 전송한 JSON이 request에 들어있는데 빼내는 방법
    data = request.json #데이터를 수신받은 것 중에서 restpull API CRUD를 resquest로 들어옴
    result = products.insert_one(data)
    return jsonify ({id: str(result.insert_id)}),201 #제이슨을 바꿔주는 역할, 파이썬을 반환값을 여러개 날려도 됨

#전체 상품 조회
def get_all_products():
    docs = products.find() # 전체 문서를 가져옴
    result = [] # 결과를 담을 빈 리스트 생성
    for doc in docs:
        conv_doc = convert_doc(doc) #_id를 id로 바꿈
        result.append(conv_doc)
    return jsonify(result)

#개별 상품 조회
def get_product_by_name(name):
    doc = products.find_one({"name":name})
    if doc:
        converted = convert_doc(doc)
        return jsonify(converted)
    else:
        return jsonify({"error" :"not found"}),404

#제품 수정
def update_product(name):
    data = request.json
    result = products.update_one({"name":name},{"$set":data}) #이름과 같으면 넘겨왔더 json데이터를 업데이트 시킴
    return jsonify ({"modify": result.modified_count})

#제품 삭제
def delete_product(name):
    result = products.delete_one({"name":name})
    return jsonify({"delete":result.deleted_count}) #1개면 1넘어오고 여러개면 여러개 넘어옴