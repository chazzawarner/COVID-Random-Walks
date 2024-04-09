import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ward import Ward
from person import Worker, Patient

def main():
    # Create a ward with 3 bays and 4 beds per bay
    ward = Ward(bays=3, beds=4)

    # Position patients in the beds
    patients = []
    for bed in ward.bed_positions:
        patient = Patient(position=bed)
        patients.append(patient)
    
    # Create a worker
    worker = Worker(patients, position=np.array([0.0,5.0]), step_length=0.5)
    
    """# Render the ward and people
    fig, ax = plt.subplots()
    ward.render(ax)
    worker.render(ax)
    for patient in patients:
        patient.render(ax)
        
    plt.show()"""
        
    # Render the ward and patients and animate the worker
    fig, ax = plt.subplots()
    ward.render(ax)
    worker_render = worker.render(ax)
    for patient in patients:
        patient.render(ax)
    
    target_render = ax.scatter(worker.target.position[0], worker.target.position[1], c='green', zorder=10)
        
    # Add time step text outside of the plot
    time_step_text = ax.text(0.02, 0.95, '', transform=fig.transFigure)
    
    def update(frame):
        # Update the worker
        worker.update(ward)
        worker_render.set_offsets([worker.position])
        
        #print(f"Worker is now in {ward.get_room(worker.position)}")
        
        # Update the target
        target_render.set_offsets([worker.target.position])
        
        # Update the time step text
        time_step_text.set_text(f'Time step: {frame}')
    
    ani = animation.FuncAnimation(fig, update, frames=100, blit=False)
    plt.show()
    

if __name__ == '__main__':
    main()