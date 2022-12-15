class Job:
    def __init__(self):
        self.companyImage = ""
        self.jobName = ""
        self.companyName = ""
        self.jobType = ""
        self.discription = ""
   
    def setCompanyImage(self , image):
        self.companyImage = image
    def setJobName(self , jobName):
        self.jobName = jobName
    def setCompanyName(self , companyName):
        self.companyName = companyName
    def setJobType(self , jobType):
        self.jobType = jobType
    def setDiscription(self , discription):
        self.discription += discription
          