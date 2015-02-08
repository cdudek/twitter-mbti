__author__ = 'calvindudek'
from eval.Evaluation import Evaluation

def main():
  e = Evaluation()
  e.readResultsFromFile()
  e.getResults()


if __name__ == "__main__":
  main()