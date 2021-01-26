from myproject import db

# Define Quotes model below
class Quotes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quoteauthor = db.Column(db.String(100), index=True)
    quotestring = db.Column(db.String(200), index=True)

    def __repr__(self):
        return "<Quote : {}>".format(self.quotestring)
  
