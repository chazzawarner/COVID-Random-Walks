import numpy as np
import matplotlib.pyplot as plt

# Define the COVID Particle class
class Particle:
    def __init__(self, creation_time, origin, spread=1, half_life=1, id=None):
        self.origin = origin
        
        # Set the particle's position
        self.position = np.random.normal(self.origin, spread)
        
        # Generate a time until the particle decays using half-life
        self.decay_time = self.generate_decay_time(half_life) + creation_time
        
    def generate_decay_time(self, half_life):
        # Calculate the decay rate/constant
        decay_rate = np.log(2) / half_life
        
        # Generate a random number between 0 and 1
        random_number = np.random.uniform(0, 1)
        
        # Calculate the decay time
        decay_time = -np.log(1 - random_number) / decay_rate
        return decay_time
    
    def update(self):
        pass
    
    
# Particle manager class
class ParticleManager:
    def __init__(self):
        self.particles = PriorityQueue()
    
    # Create particles for each source
    def create_particles(self, num_particles, creation_time, origin, spread, half_life):
        for i in range(num_particles):
            # Generate a random hexstring for the particle ID
            id = hex(np.random.randint(0, 2**63 -1))
            
            # Create the particle and add it to the queue
            particle_to_add = Particle(creation_time, origin, spread, half_life, id)
            self.particles.push(particle_to_add, particle_to_add.decay_time)
    
    # Update the particles, checking for decay
    def update(self, timestep):
        # Pop particles that have decayed
        while self.particles.queue[0][1] <= timestep:
            self.particles.pop()
    
            
            
        
    
# Priority queue class
class PriorityQueue:
    def __init__(self):
        self.queue = np.array([])
        
    # Create a queue item
    def create_queue_item(self, item, priority):
        return (item, priority)
    
    # Push an item onto the queue with a given priority
    def push(self, item, priority):
        if self.queue.size == 0:
            # Create the queue item if empty
            self.queue = np.array([self.create_queue_item(item, priority)])
        else:
            # Find the first index where the priority is greater than the new item's priority
            index = np.argmax(self.queue[:,1] > priority)
            
            # Insert the new item at the index, pushing the rest of the items back
            self.queue = np.insert(self.queue, index, self.create_queue_item(item, priority), axis=0)
    
    # Pop the first item from the queue      
    def pop(self):
        self.queue = self.queue[1:]
        
            
            
     
    
def main():
    # Create a particle manager
    particle_manager = ParticleManager()
    
    # Create some particles
    origin = np.array([0.0, 0.0])
    spread = 1
    half_life = 5
    
    particle_manager.create_particles(1000, 0, origin, spread, half_life)
    
    # Print initial particles
    print("Particles created:")
    print(particle_manager.particles.queue)
    print("")
    
    # Plot histogram of decay times
    decay_times = [p[1] for p in particle_manager.particles.queue]
    plt.hist(decay_times, bins=10)
    plt.xlabel("Decay Time")
    plt.ylabel("Frequency")
    plt.title("Histogram of Decay Times")
    plt.show()
    
    # Plot positions of particles
    positions = [p[0].position for p in particle_manager.particles.queue]
    plt.scatter([p[0] for p in positions], [p[1] for p in positions])
    plt.xlabel("X Position")
    plt.ylabel("Y Position")
    plt.title("Positions of Particles")
    plt.show()
    
    # Update the particles
    particle_manager.update(1)
    
    # Print the particles
    print(f"{len(particle_manager.particles.queue)} particles remaining after update:")
    print(particle_manager.particles.queue)
    
if __name__ == "__main__":
    main()