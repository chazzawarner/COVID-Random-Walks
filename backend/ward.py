import numpy as np
import matplotlib.pyplot as plt

# Define Ward class
class Ward:
    def __init__(self, bays, beds, bay_length=20, bay_width=10, corridor_width=5):
        self.bays = bays # Bays per side of the corridor
        self.beds = beds # Number of beds per side of each bay
        self.bay_length = bay_length
        self.bay_width = bay_width
        self.corridor_width = corridor_width
        self.corridor_length = self.bay_width * self.bays
        
        # Generate the positions of the beds
        self.bay_objects = self.generate_bays()
        print(self.bay_objects)
        print(len(self.bay_objects))
        self.bed_positions = [bed for bay in self.bay_objects for bed in bay["beds"]]
        
        self.render_ward()
        
    def render_ward(self):
        # Initialize the figure
        fig, ax = plt.subplots()

        # Set the background color to grey
        fig.patch.set_facecolor('lightgrey')

        # Plot the corridor walls, 
        ax.add_patch(plt.Rectangle((-self.corridor_width/2, 0), self.corridor_width, self.corridor_length, linewidth=1, edgecolor='black', facecolor='white'))
        
        # Plot the bays
        for i in range(self.bays):
            # Plot the bay walls
            # Left bays
            ax.add_patch(plt.Rectangle((-self.corridor_width/2 - self.bay_length, i * self.bay_width), self.bay_length, self.bay_width, linewidth=1, edgecolor='black', facecolor='white'))
            ax.text(-self.corridor_width/2 - self.bay_length/2, i * self.bay_width + self.bay_width/2, f"Bay {2*i+1}", ha='center', va='center', fontstyle='italic', fontweight='bold', fontsize=15, alpha=0.3)
            
            # Right bays
            ax.add_patch(plt.Rectangle((self.corridor_width/2, i * self.bay_width), self.bay_length, self.bay_width, linewidth=1, edgecolor='black', facecolor='white'))
            ax.text(self.corridor_width/2 + self.bay_length/2, i * self.bay_width + self.bay_width/2, f"Bay {2*i+2}", ha='center', va='center', fontstyle='italic', fontweight='bold', fontsize=15, alpha=0.3)
            
            # Plot doors
            ax.add_patch(plt.Rectangle((-self.corridor_width/2 - self.corridor_width/6, i * self.bay_width + self.bay_width/3), self.corridor_width/3, self.bay_width/3, facecolor='white'))
            ax.add_patch(plt.Rectangle((self.corridor_width/2 - self.corridor_width/6, i * self.bay_width + self.bay_width/3), self.corridor_width/3, self.bay_width/3, facecolor='white'))
        
        # Plot the beds
        bed_width = 1
        bed_length = 2
        for bed in self.bed_positions:
            ax.add_patch(plt.Rectangle((bed[0] - bed_width/2, bed[1] - bed_length/2), bed_width, bed_length, facecolor='lightblue', edgecolor='black', linewidth=1))
            #ax.plot(bed[0], bed[1], 'bo')
            
        
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
        
        plt.show()
        
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
        for i in range(self.bays):
            # Left bay
            position = (-self.corridor_width/2 - self.bay_length, i * self.bay_width)
            bays.append({
                "position": position,
                "beds": self.generate_beds(position),
                "id": f"Bay {2*i+1}"
            })
            
            # Right bay
            position = (self.corridor_width/2, i * self.bay_width)
            bays.append({
                "position": position,
                "beds": self.generate_beds(position),
                "id": f"Bay {2*i+2}"
            })
            
            
        return bays
        
        
def main():
    # Create a ward with 3 bays and 5 beds per bay
    ward = Ward(bays=3, beds=3)
    
if __name__ == "__main__":
    main()