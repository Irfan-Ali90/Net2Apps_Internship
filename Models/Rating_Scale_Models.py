# MULTIPLE SECTION MODEL, IT WORKS LIKE IF WE HAVE MULTIPLE SECTION WE MAKE MULTIPLE MODELS

class Base_Model():
    item_id = ""
    Processing_Status = ""
    Processing_Rating_Scale = ""
    Rating_Scale_Name = ""
    Rating_Scale_Description = ""
    rating_scale = ""
    option_score = ""
    option_label = ""
    option_description = ""

class Processing_Rating_Scale_section_Model(Base_Model):
    item_id = ""
    Processing_Status = ""
    Processing_Rating_Scale = ""

class Rating_Scale_Description_section_Model(Base_Model):
    Rating_Scale_Name = ""
    Rating_Scale_Description = ""

class Option_Score_section_Model(Base_Model):
    rating_scale = ""
    option_score = ""
    option_label = ""
    option_description = ""
