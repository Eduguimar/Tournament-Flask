from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

import random

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tournament.db'
db = SQLAlchemy(app)

class Tournament(db.Model): #classe Torneio
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    actual_round = db.Column(db.Integer) # rodada atual
    competitors_number = db.Column(db.Integer, nullable=False)
    matches = db.relationship('Match', backref='tournament') # lista de partidas do torneio
    competitors = db.relationship('Competitor', backref='tournament') # lista de competidores do torneio
    completed = db.Column(db.Boolean) # se o torneio foi concluído

    def __repr__(self):
        return '<Tournament %r>' % self.id

class Match(db.Model): #classe Partida
    id = db.Column(db.Integer, primary_key=True)
    round = db.Column(db.Integer) #rodada? (o que uso para incrementar isso?)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False) #linka com o torneio
    competitor_one_id = db.Column(db.Integer, db.ForeignKey('competitor.id'), nullable=False) #linka com o primeiro competidor
    competitor_two_id = db.Column(db.Integer, db.ForeignKey('competitor.id'), nullable=False) #linka com o segundo competidor
    winner_id = db.Column(db.Integer) #será que precisa linkar com o competitor id tmb?

    def __repr__(self):
        return '<Match %r>' % self.id

class Competitor(db.Model): #classe Competidor
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    tournament_id = db.Column(db.Integer, db.ForeignKey('tournament.id'), nullable=False) #linka com o torneio
    ranking =  db.relationship('Ranking', backref='competitor', uselist=False)# linka com a tabela ranking (uselist=False diz que é one-to-one)
    #será que precisa de mais algo aqui para linkar com as partidas? (tipo, criar uma lista de partidas aqui tmb)

    def __repr__(self):
        return '<Competitor %r>' % self.id

class Ranking(db.Model): #classe Posição
    id = db.Column(db.Integer, primary_key=True)
    competitor_id = db.Column(db.Integer, db.ForeignKey('competitor.id'), nullable=False) #linka com o competidor
    position = db.Column(db.Integer) #to em dúvida de como preencher aqui, visto que, no início, todos que perderem serão "últimos"

    def __repr__(self):
        return '<Ranking %r>' % self.id

# Página principal e criação de torneios
@app.route('/tournament', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        tournament_name = request.form['name']
        competitors_number = request.form['competitors_number']
        new_tournament = Tournament(name=tournament_name, competitors_number=competitors_number)

        try:
            db.session.add(new_tournament)
            db.session.commit()
            return redirect('/tournament')
        except:
            return "Houve um problema ao criar o torneio"
    else:
        tournaments = Tournament.query.all()

        return render_template('index.html', tournaments=tournaments)

# Página para visualização e adição de competidores do torneio
@app.route('/tournament/<int:id>/competitor', methods=['POST', 'GET'])
def add_competitor(id):
    tournament = Tournament.query.get_or_404(id)

    if request.method == 'POST':
        competitor_name = request.form['name']
        new_competitor = Competitor(name=competitor_name, tournament_id=tournament.id)

        try:
            db.session.add(new_competitor)
            db.session.commit()
            competitors = Competitor.query.filter_by(tournament_id=tournament.id).all()
            return render_template('create_competitor.html', tournament=tournament, competitors=competitors)
        except:
            return "Houve um problema ao adicionar o competidor"
    else:
        competitors = Competitor.query.filter_by(tournament_id=tournament.id).all()
        return render_template('create_competitor.html', tournament=tournament, competitors=competitors)

# Página da listagem de partidas de um torneio
#@app.route('/tournament/<int:id>/match', methods=['POST', 'GET'])
#def match(id):
#    tournament = Tournament.query.get_or_404(id)
#    competitors = Competitor.query.filter_by(tournament_id=tournament.id).all()
#    matches = Match.query.filter_by(tournament_id=tournament.id).all()

#    total_matches = len(competitors) / 2

#    for x in range(total_matches):



#    if request.method == 'POST':
#        shuffle_competitors = random.shuffle(competitors)
#        new_competitor = Competitor(name=competitor_name, tournament_id=tournament.id)
#
#        try:
#            return redirect('/tournament/<int:id>/match', tournament=tournament, competitors=competitors)
#        except:
#            return "Houve um problema ao criar as partidas"
#    else:
#        return render_template('match.html', tournament=tournament, competitors=competitors, matches=matches)


# ATENÇÃO - Deletar todos os registros(usado para testes)
#@app.route('/tournament/delete')
#def delete():
#    try:
#        db.session.query(Match).delete()
#        db.session.query(Competitor).delete()
#        db.session.query(Tournament).delete()
#        db.session.commit()
#        return redirect('/tournament')
#    except:
#        return "Houve um erro ao deletar os registros"

if __name__ == '__main__':
	app.run(debug=True)