from crmevent.db.base import Base
from crmevent.db.session import engine
from crmevent.models.company import Company
from crmevent.models.users import Users

def init_db():
    print("Début de l'initialisation de la base de données...")
    Base.metadata.create_all(bind=engine)
    print("Tables créées avec succès !")

if __name__ == "__main__":
    print("Lancement du script init_db.py...")
    init_db()