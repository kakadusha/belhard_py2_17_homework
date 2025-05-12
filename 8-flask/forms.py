from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField


class FormAddGallery(FlaskForm):
    name = StringField("Name")
    user_id = StringField("User ID")
    desc = StringField("Description")
    submit = SubmitField("Submit")


class FormAddPaintings(FlaskForm):
    name = StringField("Name")
    image = StringField("Image")
    size = StringField("Size")
    material = StringField("Material")
    technique = StringField("Technique")
    desc = StringField("Description")
    price = StringField("Price")
    status = StringField("Status")
    submit = SubmitField("Submit")


class FormAddUser(FlaskForm):
    name = StringField("Name")
    age = StringField("Age")
    phone = StringField("Phone")
    submit = SubmitField("Submit")
