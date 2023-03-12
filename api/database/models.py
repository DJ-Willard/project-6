from mongoengine import *


class Control_List(EmbeddedDocument):
    """
    Disregard schema and datetime for lab 3/10
    A MongoEngine EmbeddedDocument containing:
        distance: MongoEngine float field, required, (checkpoint distance in kilometers),
		location: MongoEngine string field, optional, (checkpoint location name),
		open_time: MongoEngine datetime field, required, (checkpoint opening time),
		close_time: MongoEngine datetime field, required, (checkpoint closing time).
    """
    miles  = FloatField()
    km  = FloatField(required=True)
    loc = StringField()
    open_t= StringField(required=True)
    close_t = StringField(required=True)


class Brevet(Document):
    """ 
    Disregard schema and datetime for lab 3/10
    A MongoEngine document containing:
		length: MongoEngine float field, required
		start_time: MongoEngine datetime field, required
		checkpoints: MongoEngine list field of Checkpoints, required
    """
    brevet_dist = FloatField(required=True)
    start_time = StringField(require=True)
    control_list = EmbeddedDocumentListField(Control_List)