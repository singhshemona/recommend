from . import db
from app.models import Ten_Categories, Hundred_Categories, Thousand_Categories


# def create_ten_classes():
#     start = 0
#     stop = 10
#     hundred_values_list = [i for i in range(1, 101)]

#     list_ten_all = []
#     for i in hundred_values_list:
#         list_ten = hundred_values_list[start:stop]
#         list_ten_all.append(list_ten)
#         if stop >= len(hundred_values_list):
#             return list_ten_all
#         start += 10
#         stop += 10

#     return list_ten_all        

ten_cat = Ten_Categories.query.all()
hun_cat = Hundred_Categories.query.all()
tho_cat = Thousand_Categories.query.all()


def populate_ten_classes():
    start = 0
    stop = 10
    for i in ten_cat:
        i.hundred_values = hun_cat[start:stop]
        db.session.add(i)

        start += 10
        stop += 10
    db.session.commit()
    return



def populate_hundred_classes():
    start = 0
    stop = 10
    for i in hun_cat:
        i.thousand_values = tho_cat[start:stop]
        db.session.add(i)

        start += 10
        stop += 10
    db.session.commit()
    return





# def create_ten_classes():
#     start = 0
#     stop = 10
#     hundred_values_list = [i for i in range(100)]

#     list_ten_all = []
#     for i in hundred_values_list:
#         list_ten = hundred_values_list[start:stop]
#         list_ten_all.append(list_ten)
#         if stop >= len(hundred_values_list):
#             return list_ten_all
#         start += 10
#         stop += 10

#     return list_ten_all        

# def populate_ten_classes():
#     ten_cat = Ten_Categories.query.all()
#     class_section = create_ten_classes()
#     for category in ten_cat:
#         category.hundred_values.append(class_section[category])
#         db.session.add(category)
#     db.session.commit()
#     return



# def populate_hundred_classes():
#     hun_cat = Hundred_Categories.query.all()
#     class_section = create_ten_classes()
#     for category in hun_cat:
#         category.thousand_values.append(class_section[category])
#         db.session.add(category)
#     db.session.commit()
#     return



