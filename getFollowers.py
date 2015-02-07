import json
from models.User import User
from controller.UserController import UserController

def main():
    uc = UserController()
    follower_ids = uc.getFollowers("bmw")

    for id in follower_ids:
      print "next {}".format(id)
      user = User(id, "unknown")

if __name__ == '__main__':
  main()