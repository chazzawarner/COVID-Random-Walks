import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from tqdm import tqdm
from ward import Ward
from person import Patient, Worker
from particle import ParticleManager

# Define simulation class using parameters from the project report
class Simulation:
    def __init__(self, max_timesteps=(12*60*60)/10, masked=False, initial_infected=2):
        self.max_timesteps = int(max_timesteps)
        self.masked = masked
        
        # Set COVID-19 parameters
        self.airborne_half_life = 1 # Half-life of airborne particles in hours
        self.surface_half_life = 7 # Half-life of surface particles in hours
        self.airborne_spread = 3.95
        self.surface_spread = 0.8
        self.airborne_mean_particles = 8
        self.surface_mean_particles = 2 

        # Create a ward
        self.ward = Ward(bays=2, beds=3, bay_length=12, bay_width=8, corridor_width=4)
        
        # Position patients in the beds
        vaccination_rate = 0.882
        self.patients = []
        for bed in self.ward.bed_positions:
            patient = Patient(position=bed)
            self.patients.append(patient)
            
            # Mask the patient if required
            patient.masked = self.masked
            
            # Vaccinate the patient
            if np.random.uniform(0, 1) < vaccination_rate:
                #print("Vaccinated")
                patient.vaccinated = True
            else:
                #print("Not vaccinated")
                pass
            
        # Infect random patients
        infected_patients = np.random.choice(self.patients, initial_infected, replace=False)
        for patient in infected_patients:
            patient.infected = True
            
        # Create workers
        num_workers = 7
        self.workers = []
        for i in range(num_workers):
            worker = Worker(self.patients, self.ward, position=np.array([0.0,5.0]), step_length=0.5)
            worker.masked = self.masked
            worker.vaccinated = True
            self.workers.append(worker)
            
        # Create the particle managers
        self.airborne_particles = ParticleManager(half_life=self.airborne_half_life, spread=self.airborne_spread, mean_particles=self.airborne_mean_particles, ward=self.ward)
        self.surface_particles = ParticleManager(half_life=self.surface_half_life, spread=self.surface_spread, mean_particles=self.surface_mean_particles, ward=self.ward)
        
        # Set the total number of people and infected people
        self.total_people = len(self.patients) + len(self.workers)
        self.total_infected = initial_infected
        
        # Initalise record of infected people
        self.infection_record = []
        for patient in self.patients:
            if patient.infected:
                self.infection_record.append({
                    "type": "patient",
                    "id": patient.id,
                    "timestep": 0
                })
    
        
    def run(self, render=False):  
        
        # Render components
        if render:
            # Setup the plot
            fig, ax = plt.subplots()
            ax.set_aspect('equal')
            ax.axis('off')
            
            # Render the ward
            self.ward.render(ax)
            
            # Render the people
            worker_renders = [self.workers[i].render(ax) for i in range(len(self.workers))]
            
            for patient in self.patients:
                patient.render(ax)
            
            # Render the particles
            airborne_render = self.airborne_particles.render(ax, color='hotpink')
            surface_render = self.surface_particles.render(ax, color='purple')
            
            # Render the masks
            for worker in self.workers:
                if worker.masked:
                    ax.add_patch(plt.Circle(worker.position, 0.6, facecolor='blue', zorder=8))
                    
            for patient in self.patients:
                if patient.masked:
                    ax.add_patch(plt.Circle(patient.position, 0.6, facecolor='blue', zorder=8))
            
            # Add time step text outside of the plot
            timestep_text = ax.text(0.02, 0.95, '', transform=fig.transFigure)
            
            # Add infection count text outside of the plot
            infection_text = ax.text(0.02, 0.90, '', transform=fig.transFigure)
        
        # Run the simulation until the maximum number of timesteps is reached or everyone is infected
        def update(timestep):
            # Update the workers
            for worker in self.workers:
                worker.update(timestep, self.airborne_particles, self.surface_particles, self.ward)
                
            # Update the patients
            for patient in self.patients:
                patient.update(timestep, self.airborne_particles, self.surface_particles, self.ward)
                
            # Update the particles
            self.airborne_particles.update(timestep)
            self.surface_particles.update(timestep)
            
            # Add to the infection record
            for patient in self.patients:
                if patient.infected and not any([record["id"] == patient.id for record in self.infection_record]):
                    self.infection_record.append({
                        "type": "patient",
                        "id": patient.id,
                        "timestep": timestep
                    })
                    
            for worker in self.workers:
                if worker.infected and not any([record["id"] == worker.id for record in self.infection_record]):
                    self.infection_record.append({
                        "type": "worker",
                        "id": worker.id,
                        "timestep": timestep
                    })
                    
            # Check if everyone is infected
            self.total_infected = sum([1 for patient in self.patients if patient.infected]) + sum([1 for worker in self.workers if worker.infected])
            
            if self.total_infected == self.total_people:
                print(f"Everyone is infected at timestep {timestep}")
                return False
            
            # Update the plot
            if render:
                # Update the time step text
                timestep_text.set_text(f'Time step: {timestep}/{self.max_timesteps}')
                
                # Update the infection count text
                infection_text.set_text(f'Infected: {self.total_infected}/{self.total_people} ({sum([1 for patient in self.patients if patient.infected])} patients, {sum([1 for worker in self.workers if worker.infected])} workers)')
                
                # Update the workers
                for worker_render in worker_renders:
                    worker_render.set_center((self.workers[worker_renders.index(worker_render)].position[0], self.workers[worker_renders.index(worker_render)].position[1]))
                    
                # Update the particles
                if len(self.airborne_particles.particles.items) > 0:
                    airborne_render.set_offsets([p.position for p in self.airborne_particles.particles.items])
                if len(self.surface_particles.particles.items) > 0:
                    surface_render.set_offsets([p.position for p in self.surface_particles.particles.items])
                
        if render:
            ani = animation.FuncAnimation(fig, update, frames=self.max_timesteps, blit=False)
            plt.show()
            
        else: # Run headless
            for timestep in tqdm(range(self.max_timesteps)):
                update(timestep)
                if self.total_infected == self.total_people:
                    #print(f"Infection record: {self.infection_record}")
                    #print(len(self.infection_record))
                    break
                
        
def main():
    sim = Simulation(masked=False)
    sim.run(render=True)
    
if __name__ == "__main__":
    main()