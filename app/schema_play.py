# from sqlalchemy import MetaData, create_engine
# from sqlalchemy_schemadisplay import create_schema_graph
#
# from app.extensions import db, Base
# from config import Config
# from sqlalchemy_schemadisplay import create_uml_graph
# from sqlalchemy.orm import class_mapper
# if __name__ == "__main__":
#
#
#     # lets find all the mappers in our model
#     mappers = [Base.__mapper__]
#     for attr in dir(Base):
#         if attr[0] == '_': continue
#         try:
#             cls = getattr(Base, attr)
#             mappers.append(cls.property.entity)
#         except:
#             pass
#
#     # pass them to the function and set some formatting options
#     graph = create_uml_graph(mappers,
#                              show_operations=False,  # not necessary in this case
#                              show_multiplicity_one=False  # some people like to see the ones, some don't
#                              )
#     graph.write("/Users/ashes/Documents/code/python/FishermanWithFlask/app/schema.png")
