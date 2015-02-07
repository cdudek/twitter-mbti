import json
from models.User import User
from controller.UserController import UserController
#import this
# from nlp.LogLinearClassifier import LinearClassifier

def main():
  mbti_types_list=['INFP','INFJ','INTJ','INTP','ISFJ','ISFP','ISTJ','ISTP','ENFJ','ENFP','ENTJ','ENTP','ESFJ','ESFP','ESTJ','ESTP'];

  print(mbti_types_list)


  for mbti_type in mbti_types_list:
    uc = UserController()
    user_ids = uc.getUsersBySearchTerm("mbti " + mbti_type)

    for id in user_ids:
      user = User(id, mbti_type)

if __name__ == '__main__':
  main()