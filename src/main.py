import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from ward import Ward
from person import Worker, Patient
from particle import ParticleManager

# Set COVID-19 parameters
airborne_half_life = 1
surface_half_life = 7
airborne_spread = 3.95
surface_spread = 0.8
airborne_mean_particles = 8
surface_mean_particles = 2 

masked_airborne_reduction_spread = 0.25 # Reduction in airborne spread if wearing a mask
masked_airborne_reduction_particles = (1 - 0.6) # Reduction in airborne particles if wearing a mask


def main():
    # Create a ward with 3 bays and 4 beds per bay
    ward = Ward(bays=2, beds=3, bay_length=12, bay_width=8, corridor_width=4)

    # Position patients in the beds
    patients = []
    for bed in ward.bed_positions:
        patient = Patient(position=bed, masked_airborne_reduction_spread=masked_airborne_reduction_spread, masked_airborne_reduction_particles=masked_airborne_reduction_particles)
        patients.append(patient)
        
        # Infect the patient
        if np.random.uniform(0, 1) < 0.1:
            patient.infected = True
            
        # Vaccinate the patient
        if np.random.uniform(0, 1) < 0.7:
            print("Vaccinated")
            patient.vaccinated = True
        else:
            print("Not vaccinated")
    
    
    # Create a worker
    worker = Worker(patients, ward, position=np.array([0.0,5.0]), step_length=0.5, masked_airborne_reduction_spread=masked_airborne_reduction_spread, masked_airborne_reduction_particles=masked_airborne_reduction_particles)
    worker.masked = True
    worker.vaccinated = True
    
    # Create the particle managers
    airborne_particles = ParticleManager(half_life=airborne_half_life, spread=airborne_spread, mean_particles=airborne_mean_particles, ward=ward)
    surface_particles = ParticleManager(half_life=surface_half_life, spread=surface_spread, mean_particles=surface_mean_particles, ward=ward)
    
    """# Render the ward and people
    fig, ax = plt.subplots()
    ward.render(ax)
    worker.render(ax)
    for patient in patients:
        patient.render(ax)
        
    plt.show()"""
        
    # Render the ward and patients and animate the worker
    fig, ax = plt.subplots()
    plt.axis('off')
    plt.axis('equal')
    ward.render(ax)
    worker_render = worker.render(ax)
    for patient in patients:
        patient.render(ax)
    
    # Render the worker's target
    target_render = ax.scatter(worker.target.position[0], worker.target.position[1], c='green', zorder=9)
    
    # Render the particles
    airborne_render = airborne_particles.render(ax, color='yellow')
    surface_render = surface_particles.render(ax, color='orange')
        
    # Add time step text outside of the plot
    time_step_text = ax.text(0.02, 0.95, '', transform=fig.transFigure)
    
    def update(frame):
        # Update the worker
        worker.update(frame, airborne_particles, surface_particles, ward)
        #worker_render.set_offsets([worker.position])
        worker_render.set_center((worker.position[0], worker.position[1]))
        
        # Update the patients
        for patient in patients:
            patient.update(frame, airborne_particles, surface_particles, ward)
            
        # Update the particles
        airborne_particles.update(frame)
        surface_particles.update(frame)
        
        airborne_render.set_offsets([p[0].position for p in airborne_particles.particles.queue])
        surface_render.set_offsets([p[0].position for p in surface_particles.particles.queue])
        
        
        #print(f"Worker is now in {ward.get_room(worker.position)}")
        
        # Update the target
        target_render.set_offsets([worker.target.position])
        
        # Update the time step text
        time_step_text.set_text(f'Time step: {frame}')
    
    ani = animation.FuncAnimation(fig, update, frames=100, blit=False)
    plt.show()
    

if __name__ == '__main__':
    main()