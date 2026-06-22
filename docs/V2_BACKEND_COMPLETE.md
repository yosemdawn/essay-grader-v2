# 馃帀 AI浣滄枃鎵归槄绯荤粺 V2.0 鍚庣寮€鍙戝畬鎴?
## 椤圭洰姒傝堪

鎴愬姛灏咥I浣滄枃鎵归槄绯荤粺浠嶸1.0锛圝SON鏂囦欢瀛樺偍+閭欢閫氱煡锛夊崌绾у埌V2.0锛圫QLite鏁版嵁搴撳瓨鍌?Web鏌ヨ锛夛紝瀹炵幇浜嗗畬鏁寸殑鐢ㄦ埛璁よ瘉鍜屾潈闄愮鐞嗙郴缁熴€?
---

## 鉁?宸插畬鎴愮殑鍏ぇ闃舵

### 绗竴闃舵锛氭暟鎹簱璁捐涓庢ā鍨嬪垱寤?鉁?
#### 鏁版嵁搴撹〃缁撴瀯
1. **鐢ㄦ埛琛?(users)** - 63涓敤鎴凤紙1绠＄悊鍛?+ 62瀛︾敓锛?   - 鐢ㄦ埛鍚嶃€佸瘑鐮佸搱甯岋紙bcrypt锛夈€佽鑹层€侀偖绠便€佺彮绾?   - 鏀寔婵€娲荤姸鎬佹帶鍒?
2. **浣滄枃琛?(essays)**
   - 瀛︾敓ID澶栭敭銆佷綔鏂囧浘鐗囪矾寰勩€丱CR鏂囨湰銆佷綔鏂囪姹?   - 鎻愪氦鏃堕棿鎴?
3. **鎵归槄璁板綍琛?(grading_records)**
   - 浣滄枃ID澶栭敭銆佸垎鏁般€佷紭缂虹偣銆佸缓璁?   - 鎵归槄鏂瑰紡锛圓I/manual锛夈€佸畬鏁碕SON缁撴灉

#### 鏍稿績鏂囦欢
- [`backend/app/models/database.py`](../backend/app/models/database.py:1) - SQLAlchemy ORM妯″瀷
- [`backend/app/database.py`](../backend/app/database.py:1) - 鏁版嵁搴撲細璇濈鐞?- [`backend/scripts/init_db.py`](../backend/scripts/init_db.py:1) - 鏁版嵁搴撳垵濮嬪寲鑴氭湰

---

### 绗簩闃舵锛欽WT璁よ瘉绯荤粺 鉁?
#### 璁よ瘉鏈哄埗
- **JWT Token**: HS256绠楁硶锛?灏忔椂鏈夋晥鏈?- **瀵嗙爜鍔犲瘑**: bcrypt鍝堝笇
- **鏉冮檺鎺у埗**: 鍩轰簬瑙掕壊鐨勮闂帶鍒讹紙RBAC锛?
#### 鏍稿績鏂囦欢
- [`backend/app/utils/security.py`](../backend/app/utils/security.py:1) - JWT鍜屽瘑鐮佸伐鍏?- [`backend/app/utils/dependencies.py`](../backend/app/utils/dependencies.py:1) - 渚濊禆娉ㄥ叆鍑芥暟
- [`backend/app/routes/auth.py`](../backend/app/routes/auth.py:1) - 璁よ瘉API璺敱

#### API绔偣
- `POST /api/auth/login` - 鐢ㄦ埛鐧诲綍
- `POST /api/auth/logout` - 鐢ㄦ埛鐧诲嚭
- `GET /api/auth/me` - 鑾峰彇褰撳墠鐢ㄦ埛淇℃伅
- `GET /api/auth/verify` - 楠岃瘉token鏈夋晥鎬?
---

### 绗笁闃舵锛氱敤鎴风鐞嗗姛鑳?鉁?
#### 鏍稿績鍔熻兘
- 鎵归噺瀵煎叆瀛︾敓璐﹀彿
- 缁熶竴瀵嗙爜璁剧疆/閲嶇疆
- 鐢ㄦ埛淇℃伅鏌ヨ鍜岀鐞?
#### 鏍稿績鏂囦欢
- [`backend/app/routes/users.py`](../backend/app/routes/users.py:1) - 鐢ㄦ埛绠＄悊API

#### API绔偣锛堜粎绠＄悊鍛橈級
- `POST /api/users/batch-import` - 鎵归噺瀵煎叆瀛︾敓
- `PUT /api/users/reset-password` - 閲嶇疆瀵嗙爜
- `GET /api/users/list` - 鑾峰彇鐢ㄦ埛鍒楄〃
- `GET /api/users/{user_id}` - 鑾峰彇鐢ㄦ埛璇︽儏
- `DELETE /api/users/{user_id}` - 鍒犻櫎鐢ㄦ埛

---

### 绗洓闃舵锛氭壒闃呰褰曞瓨鍌?鉁?
#### 鏍稿績鏀瑰姩
- 鉂?绉婚櫎閭欢鍙戦€佸姛鑳?- 鉁?鎵归槄缁撴灉淇濆瓨鍒版暟鎹簱
- 鉁?瀹屾暣鐨勪綔鏂?鎵归槄璁板綍鍏宠仈

#### 鏍稿績鏂囦欢
- [`backend/app/services/grading_db.py`](../backend/app/services/grading_db.py:1) - 鎵归槄鏁版嵁搴撴湇鍔?- [`backend/app/services/workflow_engine.py`](../backend/app/services/workflow_engine.py:1) - 鏇存柊鐨勫伐浣滄祦寮曟搸

#### 宸ヤ綔娴佺▼
```
涓婁紶浣滄枃 鈫?OCR璇嗗埆 鈫?LLM鎻愬彇瀛︾敓鍚?鈫?LLM鎵归槄 鈫?淇濆瓨鍒版暟鎹簱 鈫?杩斿洖缁撴灉
```

---

### 绗簲闃舵锛氭煡璇PI寮€鍙?鉁?
#### 鏍稿績鍔熻兘
- 瀛︾敓鏌ヨ鑷繁鐨勬壒闃呰褰?- 绠＄悊鍛樻煡璇㈡墍鏈?鎸囧畾瀛︾敓璁板綍
- 鎵归槄璁板綍璇︽儏鏌ヨ

#### 鏍稿績鏂囦欢
- [`backend/app/routes/records.py`](../backend/app/routes/records.py:1) - 鎵归槄璁板綍鏌ヨAPI

#### API绔偣
- `GET /api/records/my` - 瀛︾敓鏌ョ湅鑷繁鐨勮褰曪紙闇€student鏉冮檺锛?- `GET /api/records/all` - 绠＄悊鍛樻煡鐪嬫墍鏈夎褰曪紙闇€admin鏉冮檺锛?- `GET /api/records/student/{username}` - 绠＄悊鍛樻煡鐪嬫寚瀹氬鐢熻褰?- `GET /api/records/{record_id}` - 鏌ョ湅璁板綍璇︽儏锛堟潈闄愯嚜鍔ㄦ鏌ワ級

---

### 绗叚闃舵锛氭暟鎹縼绉讳笌娴嬭瘯 鉁?
#### 鏁版嵁杩佺Щ
- 鎴愬姛杩佺Щ62涓鐢熶粠JSON鍒癝QLite
- 鎵€鏈夊鐢熼粯璁ゅ瘑鐮侊細123456

#### 鏍稿績鏂囦欢
- [`backend/scripts/migrate_students.py`](../backend/scripts/migrate_students.py:1) - 鏁版嵁杩佺Щ鑴氭湰
- [`backend/scripts/test_apis.sh`](../backend/scripts/test_apis.sh:1) - API娴嬭瘯鑴氭湰

---

## 馃搳 鎶€鏈爤

### 鍚庣妗嗘灦
- **FastAPI** 0.104.1 - 楂樻€ц兘Web妗嗘灦
- **Uvicorn** 0.24.0 - ASGI鏈嶅姟鍣?- **SQLAlchemy** 2.0.23 - ORM妗嗘灦
- **Alembic** 1.13.0 - 鏁版嵁搴撹縼绉诲伐鍏凤紙宸插畨瑁咃紝鏈娇鐢級

### 瀹夊叏璁よ瘉
- **python-jose** 3.3.0 - JWT token
- **passlib** 1.7.4 - bcrypt瀵嗙爜鍔犲瘑

### AI鏈嶅姟
- **鐧惧害OCR** - 鏂囧瓧璇嗗埆
- **璞嗗寘LLM** - AI鎵归槄

---

## 馃殌 蹇€熷紑濮?
### 1. 瀹夎渚濊禆
```bash
cd backend
pip install -r requirements.txt
```

### 2. 鍒濆鍖栨暟鎹簱
```bash
cd backend
python3 scripts/init_db.py
```

### 3. 杩佺Щ瀛︾敓鏁版嵁
```bash
cd backend
python3 scripts/migrate_students.py
```

### 4. 鍚姩鏈嶅姟鍣?```bash
cd backend
python3 main.py
```

### 5. 娴嬭瘯API
```bash
bash backend/scripts/test_apis.sh
```

### 6. 璁块棶API鏂囨。
娴忚鍣ㄦ墦寮€锛歨ttp://localhost:8000/docs

---

## 馃攽 榛樿璐﹀彿

### 绠＄悊鍛樿处鍙?- 鐢ㄦ埛鍚嶏細`admin`
- 瀵嗙爜锛歚admin123`
- 瑙掕壊锛歛dmin

### 瀛︾敓璐﹀彿
- 鐢ㄦ埛鍚嶏細瀛︾敓濮撳悕锛堝锛歚寮犱笁`锛?- 瀵嗙爜锛歚123456`锛堢粺涓€榛樿瀵嗙爜锛?- 瑙掕壊锛歴tudent
- 鎬绘暟锛?2涓鐢?
---

## 馃摉 API浣跨敤绀轰緥

### 1. 绠＄悊鍛樼櫥褰?```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"admin123"}'
```

**鍝嶅簲锛?*
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "username": "admin",
    "role": "admin"
  }
}
```

### 2. 瀛︾敓鐧诲綍
```bash
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"寮犱笁","password":"123456"}'
```

### 3. 绠＄悊鍛樿幏鍙栨墍鏈夌敤鎴凤紙闇€瑕乼oken锛?```bash
TOKEN="your_admin_token_here"

curl -X GET "http://localhost:8000/api/users/list?limit=10" \
  -H "Authorization: Bearer $TOKEN"
```

### 4. 瀛︾敓鏌ョ湅鑷繁鐨勬壒闃呰褰?```bash
STUDENT_TOKEN="your_student_token_here"

curl -X GET "http://localhost:8000/api/records/my" \
  -H "Authorization: Bearer $STUDENT_TOKEN"
```

### 5. 绠＄悊鍛樻煡鐪嬫墍鏈夋壒闃呰褰?```bash
curl -X GET "http://localhost:8000/api/records/all?limit=20" \
  -H "Authorization: Bearer $ADMIN_TOKEN"
```

### 6. 绠＄悊鍛樻壒閲忓鍏ュ鐢?```bash
curl -X POST "http://localhost:8000/api/users/batch-import" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "students": [
      {"username": "娴嬭瘯瀛︾敓1", "email": "test1@qq.com", "class_name": "涓€鐝?},
      {"username": "娴嬭瘯瀛︾敓2", "email": "test2@qq.com", "class_name": "涓€鐝?}
    ],
    "default_password": "123456"
  }'
```

### 7. 绠＄悊鍛橀噸缃瘑鐮?```bash
# 閲嶇疆鎵€鏈夊鐢熷瘑鐮?curl -X PUT "http://localhost:8000/api/users/reset-password" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "new_password": "newpass123",
    "reset_all_students": true
  }'

# 閲嶇疆鎸囧畾瀛︾敓瀵嗙爜
curl -X PUT "http://localhost:8000/api/users/reset-password" \
  -H "Authorization: Bearer $ADMIN_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "usernames": ["寮犱笁", "鏉庡洓"],
    "new_password": "newpass123"
  }'
```

---

## 馃搧 鏂板鏂囦欢缁撴瀯

```
backend/
鈹溾攢鈹€ app/
鈹?  鈹溾攢鈹€ database.py              鉁?鏁版嵁搴撲細璇濈鐞?鈹?  鈹溾攢鈹€ models/
鈹?  鈹?  鈹斺攢鈹€ database.py          鉁?SQLAlchemy ORM妯″瀷
鈹?  鈹溾攢鈹€ routes/
鈹?  鈹?  鈹溾攢鈹€ auth.py              鉁?璁よ瘉API
鈹?  鈹?  鈹溾攢鈹€ users.py             鉁?鐢ㄦ埛绠＄悊API
鈹?  鈹?  鈹斺攢鈹€ records.py           鉁?鎵归槄璁板綍鏌ヨAPI
鈹?  鈹溾攢鈹€ services/
鈹?  鈹?  鈹溾攢鈹€ grading_db.py        鉁?鎵归槄鏁版嵁搴撴湇鍔?鈹?  鈹?  鈹斺攢鈹€ workflow_engine.py   馃攧 宸叉洿鏂帮紙鍘婚櫎閭欢锛?鈹?  鈹斺攢鈹€ utils/
鈹?      鈹溾攢鈹€ security.py          鉁?JWT鍜屽瘑鐮佸伐鍏?鈹?      鈹斺攢鈹€ dependencies.py      鉁?渚濊禆娉ㄥ叆
鈹溾攢鈹€ scripts/
鈹?  鈹溾攢鈹€ init_db.py               鉁?鏁版嵁搴撳垵濮嬪寲
鈹?  鈹溾攢鈹€ migrate_students.py      鉁?瀛︾敓鏁版嵁杩佺Щ
鈹?  鈹斺攢鈹€ test_apis.sh             鉁?API娴嬭瘯鑴氭湰
鈹斺攢鈹€ requirements.txt             馃攧 宸叉洿鏂?
data/
鈹斺攢鈹€ database.db                  鉁?SQLite鏁版嵁搴撴枃浠?```

---

## 馃攧 鏍稿績浠ｇ爜鏀瑰姩

### workflow_engine.py 涓昏鍙樺寲
**涔嬪墠锛圴1.0锛夛細**
```python
# 鏌ヨ瀛︾敓閭
student_email = self.student_db.get_email_by_name(student_name)

# 鍙戦€侀偖浠?email_sent = await self.email_service.send_grading_email(...)
```

**鐜板湪锛圴2.0锛夛細**
```python
# 淇濆瓨鍒版暟鎹簱
save_result = self.grading_db.save_grading_result(
    student_name=student_name,
    essay_text=essay_text,
    requirements=requirements,
    grading_result=grading_result,
    image_path=image_path
)
```

---

## 馃И 娴嬭瘯缁撴灉

### 娴嬭瘯鐨凙PI绔偣锛?涓級
1. 鉁?`/health` - 鍋ュ悍妫€鏌?2. 鉁?`POST /api/auth/login` - 绠＄悊鍛樼櫥褰?3. 鉁?`POST /api/auth/login` - 瀛︾敓鐧诲綍
4. 鉁?`GET /api/users/list` - 鑾峰彇鐢ㄦ埛鍒楄〃锛堢鐞嗗憳锛?5. 鉁?`GET /api/records/all` - 鏌ョ湅鎵€鏈夋壒闃呰褰曪紙绠＄悊鍛橈級
6. 鉁?`GET /api/records/my` - 鏌ョ湅鎴戠殑鎵归槄璁板綍锛堝鐢燂級
7. 鉁?`GET /api/records/student/{username}` - 鏌ョ湅鎸囧畾瀛︾敓璁板綍锛堢鐞嗗憳锛?8. 鉁?`GET /api/auth/verify` - Token楠岃瘉

### 娴嬭瘯杈撳嚭绀轰緥
```json
{
  "total": 63,
  "users": [
    {
      "id": 1,
      "username": "admin",
      "role": "admin",
      "is_active": true
    },
    {
      "id": 3,
      "username": "寮犱笁",
      "role": "student",
      "email": "student@example.com",
      "is_active": true
    }
  ]
}
```

---

## 馃攼 鏉冮檺璁捐

### 绠＄悊鍛樻潈闄愶紙admin锛?- 鉁?鎵归噺瀵煎叆/鍒犻櫎瀛︾敓璐﹀彿
- 鉁?閲嶇疆浠绘剰瀛︾敓瀵嗙爜
- 鉁?鏌ョ湅鎵€鏈夌敤鎴蜂俊鎭?- 鉁?鏌ョ湅鎵€鏈夋壒闃呰褰?- 鉁?鏌ョ湅浠绘剰瀛︾敓鐨勬壒闃呰褰曡鎯?- 鉁?鍙戣捣鎵归槄浠诲姟

### 瀛︾敓鏉冮檺锛坰tudent锛?- 鉁?鐧诲綍绯荤粺
- 鉁?鏌ョ湅鑷繁鐨勬壒闃呰褰曞垪琛?- 鉁?鏌ョ湅鑷繁鐨勬壒闃呰褰曡鎯?- 鉂?涓嶈兘鏌ョ湅鍏朵粬瀛︾敓鐨勮褰?- 鉂?涓嶈兘璁块棶鐢ㄦ埛绠＄悊鍔熻兘

---

## 馃摑 瀹屾暣API鍒楄〃

### 璁よ瘉妯″潡 (4涓狝PI)
| 鏂规硶 | 璺緞 | 鏉冮檺 | 璇存槑 |
|-----|------|------|------|
| POST | `/api/auth/login` | 鍏紑 | 鐢ㄦ埛鐧诲綍 |
| POST | `/api/auth/logout` | 闇€鐧诲綍 | 鐢ㄦ埛鐧诲嚭 |
| GET | `/api/auth/me` | 闇€鐧诲綍 | 鑾峰彇褰撳墠鐢ㄦ埛淇℃伅 |
| GET | `/api/auth/verify` | 闇€鐧诲綍 | 楠岃瘉token |

### 鐢ㄦ埛绠＄悊 (5涓狝PI)
| 鏂规硶 | 璺緞 | 鏉冮檺 | 璇存槑 |
|-----|------|------|------|
| POST | `/api/users/batch-import` | 绠＄悊鍛?| 鎵归噺瀵煎叆瀛︾敓 |
| PUT | `/api/users/reset-password` | 绠＄悊鍛?| 閲嶇疆瀵嗙爜 |
| GET | `/api/users/list` | 绠＄悊鍛?| 鑾峰彇鐢ㄦ埛鍒楄〃 |
| GET | `/api/users/{user_id}` | 绠＄悊鍛?| 鑾峰彇鐢ㄦ埛璇︽儏 |
| DELETE | `/api/users/{user_id}` | 绠＄悊鍛?| 鍒犻櫎鐢ㄦ埛 |

### 鎵归槄璁板綍 (4涓狝PI)
| 鏂规硶 | 璺緞 | 鏉冮檺 | 璇存槑 |
|-----|------|------|------|
| GET | `/api/records/my` | 瀛︾敓 | 鏌ョ湅鑷繁鐨勮褰?|
| GET | `/api/records/all` | 绠＄悊鍛?| 鏌ョ湅鎵€鏈夎褰?|
| GET | `/api/records/student/{username}` | 绠＄悊鍛?| 鏌ョ湅鎸囧畾瀛︾敓璁板綍 |
| GET | `/api/records/{record_id}` | 闇€鐧诲綍 | 鏌ョ湅璁板綍璇︽儏 |

### 鎵归槄澶勭悊锛堜繚鐣欏師鏈堿PI锛?| 鏂规硶 | 璺緞 | 鏉冮檺 | 璇存槑 |
|-----|------|------|------|
| POST | `/api/grading/upload-prompt` | 鍏紑 | 涓婁紶浣滄枃瑕佹眰 |
| POST | `/api/grading/upload-essays/{session_id}` | 鍏紑 | 涓婁紶瀛︾敓浣滄枃 |
| POST | `/api/grading/process-batch/{session_id}` | 鍏紑 | 寮€濮嬫壒閲忓鐞?|
| GET | `/api/grading/status/{task_id}` | 鍏紑 | 鏌ヨ浠诲姟鐘舵€?|

---

## 馃幆 V2.0鏍稿績鐗规€?
### 涓嶸1.0鐨勪富瑕佸尯鍒?
| 鐗规€?| V1.0 | V2.0 |
|------|------|------|
| 鏁版嵁瀛樺偍 | JSON鏂囦欢 | SQLite鏁版嵁搴?|
| 缁撴灉閫氱煡 | 閭欢鍙戦€?| Web鏌ヨ |
| 鐢ㄦ埛绯荤粺 | 鏃?| JWT璁よ瘉 |
| 鏉冮檺鎺у埗 | 鏃?| 瑙掕壊鏉冮檺 |
| 鏁版嵁鎸佷箙鍖?| 鏂囦欢 | 鏁版嵁搴撲簨鍔?|
| 瀛︾敓鏌ヨ | 閭 | 鐧诲綍Web鏌ョ湅 |
| 绠＄悊鍔熻兘 | 鏃?| 瀹屾暣绠＄悊鍚庡彴 |

---

## 馃捑 鏁版嵁搴撶粺璁?
### 褰撳墠鏁版嵁搴撶姸鎬?- **鏂囦欢澶у皬**: 40KB
- **鐢ㄦ埛鎬绘暟**: 63涓紙1绠＄悊鍛?+ 62瀛︾敓锛?- **琛ㄦ€绘暟**: 3涓紙users, essays, grading_records锛?
### 鏁版嵁搴撴枃浠朵綅缃?```
/home/admin/Downloads/essay-grader-v2/data/database.db
```

---

## 馃敡 閰嶇疆璇存槑

### 鐜鍙橀噺锛?env锛?```ini
# 鏁版嵁搴擄紙鑷姩閰嶇疆锛?DATABASE_PATH=/home/admin/Downloads/essay-grader-v2/data/database.db

# JWT閰嶇疆锛堝湪security.py涓級
SECRET_KEY=your-secret-key-change-in-production-2024
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_HOURS=2

# 瀵嗙爜閰嶇疆
DEFAULT_STUDENT_PASSWORD=123456
DEFAULT_ADMIN_PASSWORD=admin123
```

---

## 馃搱 鎬ц兘浼樺寲寤鸿锛堟湭鏉ワ級

1. **鏁版嵁搴撲紭鍖?*
   - 涓哄父鐢ㄦ煡璇㈠瓧娈垫坊鍔犵储寮?   - 鑰冭檻浣跨敤PostgreSQL鏇夸唬SQLite锛堢敓浜х幆澧冿級

2. **缂撳瓨鏈哄埗**
   - Redis缂撳瓨鐢ㄦ埛淇℃伅
   - 鎵归槄璁板綍缂撳瓨

3. **寮傛浼樺寲**
   - 鎵归槄浠诲姟闃熷垪锛圕elery锛?   - WebSocket瀹炴椂杩涘害鎺ㄩ€?
4. **瀹夊叏澧炲己**
   - SECRET_KEY鏀圭敤鐜鍙橀噺
   - 娣诲姞璇锋眰閫熺巼闄愬埗
   - 娣诲姞refresh token鏈哄埗

---

## 馃毀 宸茬煡闄愬埗

1. **浼氳瘽绠＄悊**
   - session_files浣跨敤鍐呭瓨瀛樺偍锛屼笉鏀寔澶氳繘绋?   - 寤鸿浣跨敤Redis鏇夸唬

2. **Token绠＄悊**
   - JWT鏃犵姸鎬侊紝鏃犳硶涓诲姩鎾ら攢
   - 鍙€冭檻娣诲姞token榛戝悕鍗曟満鍒?
3. **鏂囦欢瀛樺偍**
   - 浣滄枃鍥剧墖瀛樺偍鍦ㄦ湰鍦版枃浠剁郴缁?   - 鏈潵鍙縼绉诲埌OSS绛変簯瀛樺偍

---

## 馃帗 涓嬩竴姝ュ紑鍙戝缓璁?
### 鍓嶇寮€鍙戯紙Vue 3锛?1. 瀛︾敓绔〉闈?   - 鐧诲綍椤甸潰
   - 鎵归槄璁板綍鍒楄〃
   - 鎵归槄璇︽儏椤?
2. 绠＄悊鍛樼椤甸潰
   - 绠＄悊鍚庡彴
   - 瀛︾敓绠＄悊
   - 鎵归槄璁板綍绠＄悊
   - 鎵归噺澶勭悊鐣岄潰

### 鍔熻兘鎵╁睍
1. 鎵归槄璁板綍瀵煎嚭锛圗xcel/PDF锛?2. 鏁版嵁缁熻鍜屽彲瑙嗗寲
3. 浣滄枃瀵规瘮鍒嗘瀽
4. 鍘嗗彶璁板綍瓒嬪娍鍥?
---

## 鉁?椤圭洰浜偣

1. **瀹屾暣鐨勮璇佹巿鏉冪郴缁?*锛欽WT + 鍩轰簬瑙掕壊鐨勬潈闄愭帶鍒?2. **鏁版嵁搴撲簨鍔″畨鍏?*锛歋QLAlchemy ORM + 鑷姩鍥炴粴
3. **浠ｇ爜妯″潡鍖?*锛氭竻鏅扮殑鏈嶅姟灞傘€佽矾鐢卞眰銆佹ā鍨嬪眰鍒嗙
4. **鏄撲簬娴嬭瘯**锛氭彁渚涘畬鏁寸殑娴嬭瘯鑴氭湰鍜孉PI鏂囨。
5. **骞虫粦杩佺Щ**锛氳嚜鍔ㄥ皢鏃ф暟鎹縼绉诲埌鏂扮郴缁?
---

## 馃摓 鎶€鏈敮鎸?
### API鏂囨。
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### 鏃ュ織鏂囦欢
- 搴旂敤鏃ュ織: `logs/app.log`
- 鏈嶅姟鍣ㄦ棩蹇? `/tmp/server.log`

### 鏁版嵁搴撶鐞?```bash
# 閲嶆柊鍒濆鍖栨暟鎹簱锛堟竻绌烘墍鏈夋暟鎹級
cd backend
python3 scripts/init_db.py

# 杩佺Щ瀛︾敓鏁版嵁
python3 scripts/migrate_students.py

# 鑷畾涔夐粯璁ゅ瘑鐮?python3 scripts/migrate_students.py --password "your_password"
```

---

## 馃帄 寮€鍙戞€荤粨

### 寮€鍙戞椂闂寸嚎
- 绗竴闃舵锛氭暟鎹簱璁捐 鉁?- 绗簩闃舵锛欽WT璁よ瘉 鉁?- 绗笁闃舵锛氱敤鎴风鐞?鉁?- 绗洓闃舵锛氭壒闃呭瓨鍌?鉁?- 绗簲闃舵锛氭煡璇PI 鉁?- 绗叚闃舵锛氭祴璇曡縼绉?鉁?
### 浠ｇ爜缁熻
- 鏂板Python鏂囦欢锛?涓?- 鏂板Shell鑴氭湰锛?涓?- 淇敼鐜版湁鏂囦欢锛?涓?- 浠ｇ爜鎬昏鏁帮細~1500琛?
### 鏍稿績鎴愬氨
鉁?瀹屽叏鍘婚櫎閭欢渚濊禆  
鉁?寤虹珛瀹屾暣鐨勬暟鎹簱鏋舵瀯  
鉁?瀹炵幇JWT璁よ瘉鍜屾潈闄愮鐞? 
鉁?杩佺Щ62涓鐢熸暟鎹? 
鉁?鎵€鏈堿PI娴嬭瘯閫氳繃  

**V2.0鍚庣寮€鍙戝渾婊″畬鎴愶紒** 馃殌
