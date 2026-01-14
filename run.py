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

    translation_sources = [
        models.TranslationSource(
            source_name="Translate.ge",
            source_url="https://beta2.translate.ge/api/translate?from=ka&to=en&str=%s",
            query_format="georgian_bytes"
        )
    ]

    for ts in translation_sources:
        if db.session.query(models.TranslationSource).filter_by(source_name=ts.source_name).first() is None:
            db.session.add(ts)
            db.session.commit()


app.run(port=5111)
