class JobDetail :
    def __init__(self) :
        self.detail = ""
        self.specialities = []
        self.location = ""
        self.startdate = ""
        self.schedule = ""
    # def setDetail(self , detail):
    #     self.detail = detail

    def specialitiesPush(self , sp):
        self.specialities.append(sp)

    def setLocation(self , location):
        self.location = location
    def setStartdate(self , startdate):
        self.startdate = startdate
    def setSchedule(self , schedule):
        self.schedule = schedule

class Job:
    def __init__(self):
        self.detail = None 
        self.companyImage = ""
        self.jobName = ""
        self.companyName = ""
        self.jobType = ""
        self.description = ""
        self.contractLength = []
        self.payRate = ""
   
    def setCompanyImage(self , image):
        self.companyImage = image
    def setJobDetail(self , jobDetail:JobDetail):
        self.detail = jobDetail
    def setContractLength(self , contractLength):
        self.contractLength = contractLength
    def setPayrate(self , payRate):
        self.payRate = payRate
    def setJobName(self , jobName):
        self.jobName = jobName
    def setCompanyName(self , companyName):
        self.companyName = companyName
    def setJobType(self , jobType):
        self.jobType = jobType
    def setDescription(self , description):
        self.description += description


