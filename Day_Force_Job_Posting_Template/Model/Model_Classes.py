class Base_Model():
    #section 1:
    Item_ID = ""
    Processing_Status = ""
    Processing_Object = ""

    #section 2:
    Object_Name = ""
    Description = ""

    #section 3:
    Object_Name_Configure = ""
    Language = ""
    Job_Posting_Configure_Name = ""
    Job_Posting_Configure_Description = ""
    Header = ""
    Footer = ""

#Section 1 Model:
class Job_Posting_Processing_Model(Base_Model):
    Item_ID = ''
    Processing_Status = ''
    Processing_Object = ''

#Section 2 Model
class Job_Posting_Template_Model(Base_Model):
    Object_Name = ""
    Description = ""

#Section 3 Model
class Configure_Job_Posting_Template_Model(Base_Model):
    Object_Name_Configure = ""
    Language = ""
    Job_Posting_Configure_Name = ""
    Job_Posting_Configure_Description = ""
    Header = ""
    Footer = ""




