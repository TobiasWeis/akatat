from templates import create_app
import models

from flaskdb import db
from flask_cors import CORS

app = create_app()

# add customer if None is there
with app.app_context():
    CORS(app)

    if db.session.query(models.Customer).first() is None:
        print("Seeding customer")
        db.session.add(
                models.Customer(
                    first_name="Tobi")
                )
        db.session.commit()


app.run()
