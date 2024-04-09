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
    def __init__(self, patient_list, position=np.array([0.0,0.0]), step_length=0.1):
        super().__init__(position)
        self.type = "worker"
        self.patient_list = patient_list
        shuffle(self.patient_list)
        #print(self.patient_list)
        #print(f"Patient List: {[p.position for p in self.patient_list]}")
        self.target = self.patient_list[0]
        self.step_length = step_length
        direction = np.random.uniform(-1, 1, 2)
        self.direction = direction / np.linalg.norm(direction)
        self.previous_positions = [self.position.copy()]
        
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
            self.target = self.patient_list[0]
            target_position = self.target.position
        
        # Move the worker
        self.move(target_position, ward)
        
        
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
        
        
        
        
# Define patient class (which inherits from Person)
class Patient(Person):
    def __init__(self, position=np.array([0.0,0.0])):
        super().__init__(position)
        self.type = "patient"
    
    # Render the patient
    def render(self, ax):
        ax.plot(self.position[0], self.position[1], 'ro')
        
        
        
        
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