
class Action_chain():
    #class for performing consecutive actions over a period of time. Example: Flipping forward
    def __init__(self, controls_list: list, durations_list : list):
        self.controls = controls_list
        self.durations = durations_list
        self.complete = False
        self.index = 0
        self.current_duration = 0
        # there should be a duration in the durations for every controller given in the list. This inserts 0 for any lacking
        if len(durations_list) < len(controls_list):
            self.durations+= [0*len(controls_list)-len(durations_list)]

    def update(self, time_increment : float): #call this once per frame with delta time to recieve updated controls
        self.current_duration += time_increment
        if self.current_duration > self.durations[self.index]:
            self.index+=1
            self.current_duration = 0
            if self.index == len(self.controls):
                self.complete = True
                return self.controls[-1]

        return self.controls[self.index]
