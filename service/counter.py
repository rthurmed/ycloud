class CounterService:
    def __init__(self):
        self.count = 0
    
    def increment(self):
        self.count = self.count + 1
    
    def get_value(self):
        return self.count


counter_service = CounterService()
