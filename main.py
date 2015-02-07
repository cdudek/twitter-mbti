import json
from models.User import User
from controller.UserController import UserController
import this
from nlp.LogLinearClassifier import LinearClassifier

def main():
  mbti_type = "intj"
  uc = UserController()
  user_ids = uc.getUsersBySearchTerm("mbti " + mbti_type)

  for id in user_ids:
    user = User(id, mbti_type)


  #   Log Linear Model
  LLC = LinearClassifier()
  LLC.trainArguments(docs)
  LLC.perceptron(docs, 10)


if __name__ == '__main__':
  main()

