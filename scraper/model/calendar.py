from scraper.model.json_model import JsonModel
from scraper.model.csv_model import CSVModel

class Calendar(JsonModel, CSVModel):
  field_names = [
    'name', 
    'meeting_date', 
    'calendar_link', 
    'meeting_time', 
    'meeting_location', 
    'meeting_details', 
    'agenda', 
    'minutes', 
    'video', 
    'eComment']  

  def __init__(self, name, meeting_date, calendar_link, 
    meeting_time, meeting_location, meeting_details, agenda, 
    minutes, video, eComment):
    super().__init__()

    self.name = name
    self.meeting_date = meeting_date
    self.calendar_link = calendar_link
    self.meeting_time = meeting_time
    self.meeting_location = meeting_location 
    self.meeting_details = meeting_details
    self.agenda = agenda
    self.minutes = minutes
    self.video = video
    self.eComment = eComment

  def to_map(self):
    return {
      'name': self.name, 
      'meeting_date': self.meeting_date, 
      'calendar_link': self.calendar_link, 
      'meeting_time': self.meeting_time, 
      'meeting_location': self.meeting_location, 
      'meeting_details': self.meeting_details, 
      'agenda': self.agenda, 
      'minutes': self.minutes, 
      'video': self.video, 
      'eComment': self.eComment
    }

  

    




