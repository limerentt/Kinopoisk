from app.models import CharacterShip, Genre, GenreShip, Person, DirectorShip
class ImpFilm:
    def __init__(self, film, genres=[], directors=[], characters=[]):
        self.film = film
        self.genres = genres
        self.directors = directors
        self.characters = characters

def generate_impfilms(films, count=4):
    res = []
    block = []
    for i in range(len(films)):
        film = films[i]
        impfilm = ImpFilm(film)
        impfilm.genres = [genreship.genre for genreship in GenreShip.query.filter_by(film=film)]
        impfilm.directors = [directorship.director for directorship in DirectorShip.query.filter_by(film=film)]
        impfilm.characters = [charactership.character for charactership in CharacterShip.query.filter_by(film=film)]
        block.append(impfilm)
        if (i % count == 0 and i != 0) or i == len(films) - 1:
            res.append(block)
            block = []
    return res
