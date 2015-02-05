import json
from models.User import User
from controller.UserController import UserController
import this

def main():
  mbti_type = "intj"
  uc = UserController()
  user_ids = uc.getUsersBySearchTerm("mbti " + mbti_type)

  for id in user_ids:
    user = User(id, mbti_type)

  # user = th.getUser("calvindudek")
  # juser = json.dumps(user, indent=2)

  # result = th.search("mbti entj since:2010-12-27")

  # result = th.getUserTimeline("@calvindudek")


  # print result

  # file = open("calvindudek.json", "w")
  # json.dump(result, file, indent=2)


if __name__ == '__main__':
  main()

