from mongoengine import *

class Controls(EmbeddedDocument):
    """
    Disregard schema and datetime for lab 3/10
    A MongoEngine EmbeddedDocument containing:
        miles: MongoEngine float field, optional, (checkpoint distance in miles),
        km: MongoEngine float field, required, (checkpoint distance in kilometers),
        loc: MongoEngine string field, optional, (checkpoint location name),
        open_t: MongoEngine string field, required, (checkpoint opening time),
        close_t: MongoEngine string field, required, (checkpoint closing time).
    """
    miles = FloatField(required=False)
    km = FloatField(required=True)
    loc = StringField(required=False)
    open_t = StringField(required=True)
    close_t = StringField(required=True)

class B_Data(Document):
    """ 
    Disregard schema and datetime for lab 3/10
    A MongoEngine document containing:
        brevet_dist: MongoEngine float field, required
        start_time: MongoEngine string field, required
        control_list: MongoEngine list field of Control_List, required
    """
    brevet_dist = FloatField(required=True)
    start_time = StringField(required=True)
    control_list = EmbeddedDocumentListField(Controls)
