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
        
    # Move the worker towards the patient
    def update(self):
        # Call the parent class's update method
        super().update()
        
        # Get the current patient's position
        target_position = self.target.position
        
        # Check if the worker has reached the patient
        if self.target.type == "patient" and np.linalg.norm(self.position - target_position) < self.step_length:
            #print("Worker has reached the patient")
            
            # Roll the patient list
            self.patient_list = np.roll(self.patient_list, 1)
            
            # Set the new target
            self.target = self.patient_list[0]
            target_position = self.target.position
        
        # Move the worker
        self.move(target_position)
        
        
    def move(self, target_position):
        # Calculate the direction to the patient
        direction_to_target = target_position - self.position
        
        # Propose a new direction
        proposed_direction = np.random.uniform(-1, 1, 2)
        proposed_direction = proposed_direction / np.linalg.norm(proposed_direction)
        
        # Calculate angle between proposed direction and direction to patient
        angle = np.arccos(np.dot(direction_to_target, proposed_direction) / (np.linalg.norm(direction_to_target) * np.linalg.norm(proposed_direction)))
        #print(f"Angle: {angle} radians")
        
        # Calculate acceptance probability
        acceptance_probability = (np.pi - angle) / (np.pi)
        #print(f"Acceptance Probability: {acceptance_probability}")
        #print("")
        
        # Accept or reject the new direction
        if np.random.rand() < acceptance_probability:
            self.direction = proposed_direction
            
        # Move the worker
        self.position += self.step_length * self.direction
        
        
# Define patient class (which inherits from Person)
class Patient(Person):
    def __init__(self, position=np.array([0.0,0.0])):
        super().__init__(position)
        self.type = "patient"
        
        
        
        
def main():
    # Create a list of patients with random positions in a -10 to 10 square
    patients = [Patient(np.random.rand(2) * 20 - 10) for i in range(10)]
    
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
    
    def update(frame):
        nonlocal arrow
        worker.update()
        sc2.set_offsets([worker.position])
        target.set_offsets([worker.target.position])
        
        # Update time step text
        time_step_text.set_text(f'Time Step: {frame}')
        
        # Remove old arrow
        arrow.remove()
        
        # Create new arrow at updated position and direction
        arrow = ax.arrow(worker.position[0], worker.position[1], worker.direction[0], worker.direction[1], width=0.1, color='black')
        
        return sc2, target, time_step_text, arrow
    
    ani = animation.FuncAnimation(fig, update, frames=num_frames, blit=True)
    
    plt.show()
    
if __name__ == '__main__':
    main()