from .json_model import JsonModel

class CityCouncil(JsonModel):
  def __init__(self, name, title, start_date, 
    start_end, email, website, appointed_by):
    super().__init__()

    self.name = name
    self.title = title
    self.start_date = start_date
    self.start_end = start_end
    self.email = email
    self.website = website
    self.appointed_by = appointed_by

  def to_map(self):
    return {
      'name': self.name, 
      'title': self.title, 
      'start_date': self.start_date, 
      'start_end': self.start_end, 
      'email': self.email, 
      'website': self.website, 
      'appointed_by': self.appointed_by
    }



