
class Score:
    """ this class may or may not become how score is kept
        for now it is used to pass the high score back and
        forth between the game loop and the start menu loop
    """

    def __init__(self):
        self.top_score = self.fetch_score()


    def write_score(self):
        # open a text file replace current content w/ top_score
        # stick both of these in try/except blocks
        with open('TOP_SCORE.txt', 'w') as score_db:
            score_db.write(str(self.top_score))


    def fetch_score(self):
        # result = open a text file read content and update top_score
        # self.update_ts(resutl)
        try:
            with open('TOP_SCORE.txt', 'r') as score_db:
                return int(score_db.read())
        except ValueError:
            return 0

    def update_ts(self, score):
        self.top_score = score
        self.write_score()


scores = Score()
