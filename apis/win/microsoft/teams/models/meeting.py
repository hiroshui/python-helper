class Meeting:
    
    name = None
    date = None
    time_from = None
    time_until = None
    attendees = []
    
    def __init__(self, name, date, time_from, time_until, attendees:list):
        self.name = name
        self.date = date
        self.time_from = time_from
        self.time_until = time_until
        self.attendees = attendees
    
    def __str__(self):
        return f"{self.name} on {self.date} from {self.time_from} to {self.time_until} with {self.attendees}"