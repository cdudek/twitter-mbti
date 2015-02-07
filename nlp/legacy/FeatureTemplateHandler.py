__author__ = 'calvindudek'

class FTHandler():
  def __init__(self):
    self.ft = list()

  def createTriggerFeaturesWithTemplates(self, sentence, ec, label):

    ft_list = list()
    args = ec.getArguments()

    num_of_mentions = self.numMentionsTemplate(sentence, ec, label)
    stem_ec = self.StemTemplate(sentence, ec, label)

    ft_list.append(stem_ec)
    ft_list.append(num_of_mentions)
    ft_list.append(self.PosTemplate(sentence, ec, label))
    ft_list.append(self.PrevWordStemTemplate(sentence, ec, label))
    ft_list.append(self.NextWordStemTemplate(sentence, ec, label))


    for arg in args:
      stem_of_argument = self.StemInArguments(sentence, arg, label)
      ft_list.append(stem_ec + stem_of_argument)
      # pos_of_argument = self.PosInArguments(sentence, arg, label)
      # ft_list.append(stem_of_argument)
      # ft_list.append(pos_in_arguments)


    # ft_list.append(stem_template + num_of_mentions)
    # mentions = sentence.getMentions()
    # ft_list.append(self.UnigramTemplate(sentence, ec, label))


    return ft_list


  def createArgumentFeaturesWithTemplates(self, sentence, arg, ec, label):
    arg_ft_list = list()

    stem_arg = self.StemTemplate(sentence, arg, label)
    stem_of_ec = self.StemTemplate(sentence, ec, label)
    num_of_mentions = self.numMentionsTemplate(sentence, ec, label)
    #
    arg_ft_list.append(num_of_mentions)
    arg_ft_list.append(stem_of_ec)
    arg_ft_list.append(stem_arg)
    arg_ft_list.append(self.PrevWordStemTemplate(sentence, arg, label))
    # pos_of_ec = self.PosTemplate(sentence, ec, label)
    # arg_ft_list.append(self.PosTemplate(sentence, arg, label))
    # arg_ft_list.append(self.UnigramTemplate(sentence, arg, label))
    # arg_ft_list.append(pos_of_ec)
    # arg_ft_list.append(self.NextWordStemTemplate(sentence, arg, label))

    return arg_ft_list

  def UnigramTemplate(self, sentence, ec, label):
    return "l: %s f:UNIGRAM w: %s" % (label, sentence.getTokensInWords(ec.begin, ec.end))

  def StemTemplate(self, sentence, ec, label):
    return "l: %s f:STEM s: %s" % (label, sentence.getTokensInStems(ec.begin,ec.end))

  def PosTemplate(self, sentence, ec, label):
    return "l: %s f:POS p: %s" % (label, sentence.getToken(ec.begin).pos)

  def numMentionsTemplate(self, sentence, ec, label):
    return "l: %s f:NUMMENTIONS s: %d" % (label, len(sentence.getMentions()))

  def StemInArguments(self, sentence, arg, label):
    return "l: %s f:STEMINARGUMENTS s: %s" % (label, sentence.getTokensInStems(arg.begin,arg.end))

  def PosInArguments(self, sentence, arg, label):
    return "l: %s f:POSINARGUMENTS s: %s" % (label, sentence.getToken(arg.begin).pos)

  def LabelInMention(self, sentence, mention, label):
    return "l: %s f:MENTIONWORD w: %s" % (label, mention.label)

  def WordInMention(self, sentence, mention, label):
    return "l: %s f:MENTIONLABEL l: %s" % (label, sentence.getTokensInWords(mention.begin, mention.end))

  def StemInMention(self, sentence, mention, label):
    return "l: %s f:MENTIONLABEL l: %s" % (label, sentence.getTokensInStems(mention.begin, mention.end))

  def PrevWordStemTemplate(self, sentence, ec, label):
    try:
      return "l: %s f:PREVWORDSTEM s: %s" % (label, sentence.getToken(ec.begin - 1).stem)
    except:
      return "l: %s f:PREVWORDSTEM s: %s" % (label, "<START>")

  def NextWordStemTemplate(self, sentence, ec, label):
    try:
      return "l: %s f:PREVWORDSTEM s: %s" % (label, sentence.getToken(ec.begin + 1).stem)
    except:
      return "l: %s f:NEXTWORDSTEM s: %s" % (label, "</STOP>")


