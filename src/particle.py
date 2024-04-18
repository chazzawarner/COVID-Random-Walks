import numpy as np
import matplotlib.pyplot as plt

# Define the COVID Particle class
class Particle:
    def __init__(self, creation_time, origin, spread=1, half_life=1, room=None):
        self.origin = origin
        
        # Set the particle's position
        self.position = np.random.normal(self.origin, spread)
        
        # Generate a time until the particle decays using half-life
        self.decay_time = self.generate_decay_time(half_life) + creation_time
        
        self.room = room
        
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

    
# Particle manager class for one type of particle
class ParticleManager:
    def __init__(self, half_life, spread, mean_particles, ward):
        self.particles = PriorityQueue()
        self.half_life = half_life
        self.spread = spread
        self.mean_particles = mean_particles
        self.get_room = ward.get_room
    
    # Create particles for each source
    def create_particles(self, creation_time, origin, masked_reduction_particles=1, masked_reduction_spread=1):
        num_particles = round(np.random.poisson(self.mean_particles) * masked_reduction_particles)
        origin_room = self.get_room(origin)
        
        for i in range(num_particles):
            # Create the particle and add it to the queue if it is in the same room as the source
            particle_to_add = Particle(creation_time, origin, self.spread * masked_reduction_spread, self.half_life, origin_room)
            particle_room = self.get_room(particle_to_add.position)
            
            if particle_room == origin_room:
                self.particles.push(particle_to_add, particle_to_add.decay_time)
    
    # Update the particles, checking for decay
    def update(self, timestep):
        # Pop particles that have decayed
        if len(self.particles.queue) > 0:
            while self.particles.queue[0][1] <= timestep:
                self.particles.pop()
            
    # Render the particles
    def render(self, ax, color='red'):
        # Get the positions of the particles
        particle_positions = [p[0].position for p in self.particles.queue]
        
        # Plot the particles
        return ax.scatter([p[0] for p in particle_positions], [p[1] for p in particle_positions], c=color, alpha=0.5, s=0.5, zorder=7)
        
    
    # Check for particles in a radius using sweep and prune
    def check_for_particles(self, position, radius):
        # Get the particles in the room
        position_room = self.get_room(position)
        room_particles = [p for p in self.particles.queue if p[0].room == position_room]
        room_particles = [p[0].position for p in room_particles]
        
        # Reject particles outside radius on x-axis
        min_x = position[0] - radius
        max_x = position[0] + radius
        
        # Get the particles within the x range
        within_x = [p for p in room_particles if p[0] >= min_x and p[0] <= max_x]
        
        # Reject particles outside radius on y-axis
        min_y = position[1] - radius
        max_y = position[1] + radius
        
        # Get the particles within the y range
        within_y = [p for p in within_x if p[1] >= min_y and p[1] <= max_y]
        
        # Find particles within the radius
        within_radius = [p for p in within_y if np.linalg.norm(np.array(p) - np.array(position)) <= radius]
        
        # Return the particles within the radius
        return within_radius
    
    
# Priority queue class
class PriorityQueue: 
    def __init__(self):
        self.items = np.array([])
        self.priorities = np.array([])
        
    # Push an item onto the queue with a given priority
    def push(self, item, priority):
        # If the queue is empty, initialise the items and priorities arrays with the new item and its priority
        if self.items.size == 0:
            self.items = np.array([item])
            self.priorities = np.array([priority])
        else:
            # Find the indices of the items with a higher priority than the new item
            higher_priority_indices = np.argwhere(self.priorities > priority)
            
            # If there are no items with a higher priority, append the new item at the end
            if higher_priority_indices.size == 0:
                index_to_push = self.items.size
            else:
                # Otherwise, insert the new item at the position of the first item with a higher priority
                index_to_push = higher_priority_indices[0]
            
            # Insert the new item and its priority at the calculated index
            self.items = np.insert(self.items, index_to_push, item, axis=0)
            self.priorities = np.insert(self.priorities, index_to_push, priority)
        
    # Pop the first item from the queue
    def pop(self):
        self.items = self.items[1:]
        self.priorities = self.priorities[1:]
        
    
    
def main():
    # Create some particles
    origin = np.array([0.0, 0.0])
    spread = 1
    half_life = 5
    
    # Create a particle manager
    particle_manager = ParticleManager(half_life, spread, 1)
    
    particle_manager.create_particles(1000, origin)
    
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
    #main()
    pass