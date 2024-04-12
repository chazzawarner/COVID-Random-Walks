import numpy as np
from numpy.random import shuffle
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define the Person class
class Person:
    def __init__(self, position=np.array([0.0,0.0]), infected=False, masked=False, vaccinated=True):
        self.position = position
        self.infected = infected
        self.masked = masked
        self.vaccinated = vaccinated
    
    def update(self):
        pass
    
    def render(self, ax):
        pass
        
# Define healthcare worker class (which inherits from Person)
class Worker(Person):
    def __init__(self, patient_list, ward, position=np.array([0.0,0.0]), step_length=0.1):
        super().__init__(position)
        self.type = "worker"
        self.patient_list = patient_list
        shuffle(self.patient_list)
        self.step_length = step_length
        direction = np.random.uniform(-1, 1, 2)
        self.direction = direction / np.linalg.norm(direction)
        self.previous_positions = [self.position.copy()]
        
        # Set the target patient and path
        self.target_patient = self.patient_list[0]
        self.path = self.get_path(self.position, self.target_patient, ward)
        self.target = self.path[0]
        
    # Render the worker
    def render(self, ax):
        return ax.scatter(self.position[0], self.position[1], c='blue')
        
    # Move the worker towards the patient
    def update(self, ward):
        # Call the parent class's update method
        super().update()
        
        target_position = self.target.position
        
        # Check if the worker has reached the patient
        if self.target.type == "patient" and np.linalg.norm(self.position - self.target.position) < self.step_length:
            #print("Worker has reached the patient")
            
            # Roll the patient list
            self.patient_list = np.roll(self.patient_list, 1)
            
            # Set the new target
            self.target_patient = self.patient_list[0]
            self.path = self.get_path(self.position, self.target_patient, ward)
            self.target = self.path[0]
            target_position = self.target.position
        
        # Check if the worker has reached a point on its path
        elif self.target.type == "path" and np.linalg.norm(self.position - self.target.position) < self.step_length:
            #print("Worker has reached a point on its path")
            
            # Set the new target
            self.target = self.path[self.path.index(self.target) + 1]
            target_position = self.target.position
        
        # Move the worker
        self.move(target_position, ward)
        
    # Try to move the worker in the direction of the target
    def move(self, target_position, ward):
        # Calculate the direction to the patient
        direction_to_target = target_position - self.position
        
        # Propose a new direction that is within the ward and ensure the worker will make a valid move (if accepted)
        while True:
            proposed_direction = np.random.uniform(-1, 1, 2)
            proposed_direction /= np.linalg.norm(proposed_direction)
            new_position = self.position + self.step_length * proposed_direction

            if self.check_move(self.position, new_position, ward):
                break
        
        
        ### MAKE IT SO THE WORKER CAN ONLY MOVE WITHIN ITS CURRENT ROOM AND INTO THE NEXT
        
        # Calculate angle between proposed direction and direction to patient
        angle = np.arccos(np.dot(direction_to_target, proposed_direction) / (np.linalg.norm(direction_to_target) * np.linalg.norm(proposed_direction)))
        #print(f"Angle: {angle} radians")
        
        # Calculate acceptance probability
        acceptance_probability = (np.pi - angle) / (np.pi)
        
        # Accept or reject the new direction
        random_value = np.random.uniform(0, 1)
        if random_value < acceptance_probability:
            self.direction = proposed_direction
            
        # Move the worker if the new direction is valid
        if self.check_move(self.position, self.position + self.step_length * self.direction, ward):
            self.position += self.step_length * self.direction
        #self.position += self.step_length * self.direction
        
        # Add the new position to the list of previous positions
        self.previous_positions.append(self.position.copy())
        
    # Check if the worker will make a valid move
    def check_move(self, position, proposed_position, ward):
        #print(f"Checking move from {position} to {proposed_position}")
        current_room = ward.get_room(position)
        proposed_room = ward.get_room(proposed_position)
        
        #print(f"Current Room: {current_room}")
        #print(f"Proposed Room: {proposed_room}")
        
        # Check if the worker is moving inside the same room
        if current_room == proposed_room:
            #print("Worker is moving inside the same room")
            return True
        
        # Check if the worker is moving outside
        elif proposed_room == "Outside":
            #print("Worker is trying to moving outside")
            return False
        
        # Check if the worker is moving to a different bay (ie. through the walls)
        elif "Bay" in current_room and "Bay" in proposed_room:
            #print("Worker is trying to move through the walls")
            return False
        
        # Else, the worker is moving between a bay and the corridor
        else:
            #print("Worker is moving between a bay and the corridor")
            return True
        
    # Get the path to the next patient
    def get_path(self, position, target_patient, ward):
        path = []
        
        # Get the worker's bay
        worker_bay = ward.get_room(position)
        if worker_bay != "Corridor":
            worker_bay = int(worker_bay.split(" ")[1])
            
        # Get the target patient's bay
        patient_bay = ward.get_room(target_patient.position)
        patient_bay = int(patient_bay.split(" ")[1])
        
        # Check if the worker is in the same room as the target patient
        if ward.get_room(position) == ward.get_room(target_patient.position):
            path.append(target_patient)
            return path
        
        # Get spine points of the ward
        spine_points = ward.ward_spine
        
        # Find the spine point for the target patient's bay
        if patient_bay % 2 == 0:
            patient_spine = spine_points[patient_bay // 2 - 1]
        else:
            patient_spine = spine_points[patient_bay // 2]
        
        # If the worker is not in the corridor, find the bay
        if not worker_bay == "Corridor":
            # Find the spine point for the worker's current bay
            if worker_bay % 2 == 0:
                worker_spine = spine_points[worker_bay // 2 - 1]
            else:
                worker_spine = spine_points[worker_bay // 2]
            
            # If the worker's bay and the target's bay are directly opposite each other
            #if worker_spine == patient_spine:
            if worker_bay // 2 == patient_bay // 2 - 1 or worker_bay // 2 - 1 == patient_bay // 2:
                path.append(target_patient)
                return path
            
            # Else, the worker must move through the spine points
            path.append(Path(worker_spine))
        
        # Add the target patient's spine point and position to the path
        path.append(Path(patient_spine))
        path.append(target_patient)
            
        print(f"Path: {path}")
        
        return path
        
        
        
        
# Define patient class (which inherits from Person)
class Patient(Person):
    def __init__(self, position=np.array([0.0,0.0])):
        super().__init__(position)
        self.type = "patient"
    
    # Render the patient
    def render(self, ax):
        ax.plot(self.position[0], self.position[1], 'ro')
        
class Path:
    def __init__(self, position, type="path"):
        self.position = position
        self.type = type
        
        
def main():
    # Create a list of patients with random positions in a -10 to 10 square
    bounds = np.array([[-10, 10], [-10, 10]])
    patients = [Patient(np.random.rand(2) * 20 - 10) for _ in range(10)]
    
    # Create a worker
    worker = Worker(patients)
    
    # Initialise animation
    num_frames = 100
    fig, ax = plt.subplots()
    ax.set_xlim(-10, 10)
    ax.set_ylim(-10, 10)
    
    # Plot patients and worker
    sc = ax.scatter([p.position[0] for p in patients], [p.position[1] for p in patients], c='red')
    sc2 = ax.scatter(worker.position[0], worker.position[1], c='blue')
    
    # Plot target
    target = ax.scatter(worker.target.position[0], worker.target.position[1], c='green')
    
    # Add text for time step
    time_step_text = ax.text(0.02, 0.95, '', transform=ax.transAxes)
    
    # Add arrow for worker direction
    arrow = ax.arrow(worker.position[0], worker.position[1], worker.direction[0], worker.direction[1], width=0.1, color='black')

    # Plot the worker's path
    worker_path = ax.plot([p[0] for p in worker.previous_positions], [p[1] for p in worker.previous_positions], c='gray')
    
    def update(frame):
        nonlocal arrow
        worker.update(bounds=bounds)
        sc2.set_offsets([worker.position])
        target.set_offsets([worker.target.position])
        
        # Update time step text
        time_step_text.set_text(f'Time Step: {frame}')
        
        # Remove old arrow
        arrow.remove()
        
        # Create new arrow at updated position and direction
        arrow = ax.arrow(worker.position[0], worker.position[1], worker.direction[0], worker.direction[1], width=0.1, color='black')
        
        # Update worker path
        worker_path[0].set_data([p[0] for p in worker.previous_positions], [p[1] for p in worker.previous_positions])
        
        return sc2, target, time_step_text, arrow, worker_path[0]
    
    ani = animation.FuncAnimation(fig, update, frames=num_frames, blit=True)
    
    plt.show()
    
if __name__ == '__main__':
    main()