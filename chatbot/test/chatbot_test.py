from chatbot.config.DatabaseConfig import *
from chatbot.utils.Database import Database
from chatbot.utils.Preprocess import Preprocess

# 전처리 객체 생성
p = Preprocess(word2index_dic='C:/Users/obybk/OneDrive/바탕 화면/AI/deepChat/chatbot/train_tools/dict/chatbot_dict.bin',
 userdic='C:/Users/obybk/OneDrive/바탕 화면/AI/deepChat/Tokenizing/user_dic.txt')

# 질문/답변 학습 디비 연결 객체 생성
db = Database(
    host=DB_HOST, user=DB_USER, password=DB_PASSWORD, db_name=DB_NAME
)
db.connect()    # 디비 연결

# 원문
# query = "오전에 탕수육 10개 주문합니다"
# query = "화자의 질문 의도를 파악합니다."
# query = "안녕하세요"
query = "오전에 탕수육 10개 주문할게요"

# 의도 파악
from chatbot.models.intent.IntentModel import IntentModel
intent = IntentModel(model_name='C:/Users/obybk/OneDrive/바탕 화면/AI/deepChat/intent_model.h5', proprocess=p)
predict = intent.predict_class(query)
intent_name = intent.labels[predict]

# 개체명 인식
from chatbot.models.ner.NerModel import NerModel
ner = NerModel(model_name='C:/Users/obybk/OneDrive/바탕 화면/AI/deepChat/ner_model.h5', proprocess=p)
predicts = ner.predict(query)
ner_tags = ner.predict_tags(query)

print("질문 : ", query)
print("=" * 100)
print("의도 파악 : ", intent_name)
print("개체명 인식 : ", predicts)
print("답변 검색에 필요한 NER 태그 : ", ner_tags)
print("=" * 100)

# 답변 검색
from chatbot.utils.FindAnswer import FindAnswer

try:
    f = FindAnswer(db)
    answer_text, answer_image = f.search(intent_name, ner_tags)
    answer = f.tag_to_word(predicts, answer_text)
except:
    answer = "죄송해요 무슨 말인지 모르겠어요"

print("답변 : ", answer)

db.close() # 디비 연결 끊음




