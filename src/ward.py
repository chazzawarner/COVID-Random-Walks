import numpy as np
import matplotlib.pyplot as plt

# Define Ward class
class Ward:
    def __init__(self, bays, beds, bay_length=20, bay_width=10, corridor_width=5):
        self.num_bays = bays # Bays per side of the corridor
        self.beds = beds # Number of beds per side of each bay
        self.bay_length = bay_length
        self.bay_width = bay_width
        self.corridor_width = corridor_width
        self.corridor_length = self.bay_width * self.num_bays
        
        # Generate the positions of the beds
        self.bays, self.bed_positions, self.bay_positions = self.generate_bays()
        #print(self.bed_positions)
        
        # Generate corridor
        self.corridor = plt.Rectangle((-self.corridor_width/2, 0), self.corridor_width, self.corridor_length, linewidth=1, edgecolor='black', facecolor='white')
        self.corridor_position = (
            (-self.corridor_width/2, 0),
            (self.corridor_width/2, 0),
            (self.corridor_width/2, self.corridor_length),
            (-self.corridor_width/2, self.corridor_length)
        )
        
        #self.render_ward()
        
        self.ward_spine = self.create_spine()
        
    def render_ward(self):
        # Initialise the figure
        fig, ax = plt.subplots()

        # Set the background color to grey
        fig.patch.set_facecolor('lightgrey')
        
        # Render the ward
        self.render(ax, internal_render=True)
        
        plt.show()
        
        
    def render(self, ax, internal_render=False):
        # Plot the corridor walls, 
        ax.add_patch(self.corridor)
        
        # Plot the bays
        for i in range(len(self.bays)):
            # Plot bays
            ax.add_patch(self.bays[i])
            text_position = (self.bays[i].get_x() + self.bays[i].get_width()/2, self.bays[i].get_y() + self.bays[i].get_height()/2)
            ax.text(text_position[0], text_position[1], f"Bay {i+1}", ha='center', va='center', fontstyle='italic', fontweight='bold', fontsize=15, alpha=0.3)
     
            # Plot doors
            if i % 2 == 0:
                ax.add_patch(plt.Rectangle((self.bays[i].get_x() + self.bays[i].get_width() - self.corridor_width/6, self.bays[i].get_y() + self.bays[i].get_height()/3), self.corridor_width/3, self.bay_width/3, facecolor='white'))
            else:
                ax.add_patch(plt.Rectangle((self.bays[i].get_x() - self.corridor_width/6, self.bays[i].get_y() + self.bays[i].get_height()/3), self.corridor_width/3, self.bay_width/3, facecolor='white'))
        
        # Plot the beds
        bed_width = 1
        bed_length = 2
        for bed in self.bed_positions:
            ax.add_patch(plt.Rectangle((bed[0] - bed_width/2, bed[1] - bed_length/2), bed_width, bed_length, facecolor='lightblue', edgecolor='black', linewidth=1, zorder=5))
            #ax.plot(bed[0], bed[1], 'bo')
            
        if internal_render:
            # Plot the spine
            ax.scatter(self.ward_spine[:,0], self.ward_spine[:,1], c='black', zorder=10)
            
            # Set the axis limits
            padding = 1.1
            """ax.set_xlim((-self.corridor_width/2 - self.bay_length) * padding, (self.corridor_width/2 + self.bay_length) * padding)
            ax.set_ylim(-self.corridor_length * (padding - 1), self.corridor_length * padding)"""
            ax.set_xlim(-self.corridor_width/2 - self.bay_length, self.corridor_width/2 + self.bay_length)
            ax.set_ylim(0, self.corridor_length)
            
            # Set the aspect ratio to be equal
            ax.set_aspect('equal')
            
            # Remove the axes
            ax.axis('off')
        
    # Generate the positions of the beds in a bay
    def generate_beds(self, bay_position):
        bed_positions = []
        bed_length = 1
        
        for i in range(self.beds):
            x_positions = np.linspace(0, self.bay_length, self.beds+1)
            x_positions += self.bay_length/self.beds/2
            
            y_positions = np.linspace(bed_length, self.bay_width - bed_length, 2)
            
            # Top row of beds
            bed_positions.append((x_positions[i], y_positions[0]))
            
            # Bottom row of beds
            bed_positions.append((x_positions[i], y_positions[1]))
            
            
        for i in range(len(bed_positions)):
            bed_positions[i] = (bed_positions[i][0] + bay_position[0], bed_positions[i][1] + bay_position[1])
        
        return bed_positions
            
    
    # Generate the positions of the bays
    def generate_bays(self):
        bays = []
        beds = []
        bay_positions = []
        for i in range(self.num_bays):
            # Left bay
            position = (-self.corridor_width/2 - self.bay_length, i * self.bay_width)
            bays.append(plt.Rectangle(position, self.bay_length, self.bay_width, facecolor='white', edgecolor='black', linewidth=1))
            beds.extend(self.generate_beds(position))
            
            ## Add the bay position, counter-clockwise from the bottom left
            bay_positions.append([
                (position[0], position[1]),
                (position[0] + self.bay_length, position[1]),
                (position[0] + self.bay_length, position[1] + self.bay_width),
                (position[0], position[1] + self.bay_width)
            ])
            
            # Right bay
            position = (self.corridor_width/2, i * self.bay_width)
            bays.append(plt.Rectangle(position, self.bay_length, self.bay_width, facecolor='white', edgecolor='black', linewidth=1))
            beds.extend(self.generate_beds(position))
            
            ## Add the bay position (as above)
            bay_positions.append([
                (position[0], position[1]),
                (position[0] + self.bay_length, position[1]),
                (position[0] + self.bay_length, position[1] + self.bay_width),
                (position[0], position[1] + self.bay_width)
            ])
            
        return bays, beds, bay_positions
    
    # Find the room (bay or corridor) that a position is in
    def get_room(self, position):
        
        # Check if the position is in a bay
        for i in range(len(self.bay_positions)):
            if position[0] >= self.bay_positions[i][0][0] and position[0] <= self.bay_positions[i][1][0] and position[1] >= self.bay_positions[i][0][1] and position[1] <= self.bay_positions[i][2][1]:
                return f"Bay {i+1}"
            
        # Check if the position is in the corridor
        if position[0] >= self.corridor_position[0][0] and position[0] <= self.corridor_position[1][0] and position[1] >= self.corridor_position[0][1] and position[1] <= self.corridor_position[2][1]:
            return "Corridor"
        
        return "Outside"
        
    # Create the spine points of the ward
    def create_spine(self):
        # Distribute the spine points along the y-axis
        spine_y = np.linspace(self.bay_width/2, self.corridor_length - self.bay_width/2, self.num_bays)
        
        # Create the spine points
        spine = [(0, y) for y in spine_y]
        return np.array(spine)
        
def main():
    # Create a ward with 3 bays and 5 beds per bay
    ward = Ward(bays=3, beds=4)
    ward.render_ward()
    
if __name__ == "__main__":
    main()