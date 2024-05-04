import numpy as np
import matplotlib.pyplot as plt
from sim import Simulation

# Get simulation results and save to a csv file if required
def get_simulation_results(masked=False, repeat_sims=25, save_results=False):
    sim_results = []
    repeat_sims = repeat_sims # Number of simulations to run
    for i in range(repeat_sims):
        sim = Simulation(masked=masked)
        print(f"Running simulation {i+1} of {repeat_sims}")
        sim.run()
        sim_results.append(sim.infection_record)
        
    print(f"Complete {repeat_sims} simulations")
    print(f"Average number of infections: {np.mean([len(sim_result) for sim_result in sim_results])}")
    
    # Save the results to a csv file if required
    if save_results:
        with open("data/results.csv", "w") as file:
            file.write("Simulation,Type,ID,Timestep\n")
            for i, sim_result in enumerate(sim_results):
                for record in sim_result:
                    file.write(f"{i},{record['type']},{record['id']},{record['timestep']}\n")
    
    return sim_results
                    
# Plot simulation results
def plot_simulation_results(sim_results, plot_average=False, plot_percentiles=False, plot_simulations=True):
    total_people = len(sim_results[0])
    
    # Plot the results for each simulation
    if plot_simulations:
        for sim_result in sim_results:
            x = [record["timestep"] for record in sim_result]
            y = [i / total_people * 100 for i in range(len(x))]
            if sim_results.index(sim_result) == 0:
                plt.plot(x, y, '--', alpha=0.5, label="Simulation Result", color='red', zorder=1)
            else: 
                plt.plot(x, y, '--', alpha=0.5, color='red', zorder=1)
        
    # Plot the average number of infections and percentiles for each timestep
    if plot_average or plot_percentiles:
        timesteps = np.arange(0, np.max([record["timestep"] for sim_result in sim_results for record in sim_result]) + 1)
        average_infections = np.empty(len(timesteps))
        lower_percentile = np.empty(len(timesteps))
        upper_percentile = np.empty(len(timesteps))
        for timestep in timesteps:
            infections_at_timestep = [np.interp(timestep, [record["timestep"] for record in sim_result], [i for i in range(len(sim_result))]) for sim_result in sim_results]
            average_infections[timestep] = np.mean(infections_at_timestep)
            lower_percentile[timestep] = np.percentile(infections_at_timestep, 15.87)
            upper_percentile[timestep] = np.percentile(infections_at_timestep, 84.13)
        
        if plot_percentiles:
            plt.fill_between(timesteps, lower_percentile / total_people * 100, upper_percentile / total_people * 100, alpha=0.3, color='red', label=r"1 $\sigma$ error on average", zorder=2)
        
        if plot_average:
            plt.plot(timesteps, average_infections / total_people * 100, label="Average", color='red', zorder=3)
    
        
    plt.xlabel("Timestep")
    plt.ylabel("Percentage of people infected (%)")
    plt.legend(loc="lower right")
    #plt.xscale("log") 
    
    plt.savefig("plots/unmasked_25_results.pdf", format='pdf')
    plt.show()

# Load results from a csv file
def load_simulation_results(filename):
    sim_results = []
    with open(filename, "r") as file:
        lines = file.readlines()
        num_sims = int(lines[-1].split(",")[0]) + 1
        #print(f"Number of simulations: {num_sims}")
        
        for i in range(num_sims):
            sim_results.append([{
                "type": line.split(",")[1],
                "id": line.split(",")[2],
                "timestep": int(line.split(",")[3])
            } for line in lines if line.split(",")[0] == str(i)])

    return sim_results

# Get average and percentiles for each timestep
def get_average_and_percentiles(sim_results):
    total_people = len(sim_results[0])
    timesteps = np.arange(0, np.max([record["timestep"] for sim_result in sim_results for record in sim_result]) + 1)
    average_infections = np.empty(len(timesteps))
    lower_percentile = np.empty(len(timesteps))
    upper_percentile = np.empty(len(timesteps))
    for timestep in timesteps:
        infections_at_timestep = [np.interp(timestep, [record["timestep"] for record in sim_result], [i for i in range(len(sim_result))]) for sim_result in sim_results]
        average_infections[timestep] = np.mean(infections_at_timestep)
        lower_percentile[timestep] = np.percentile(infections_at_timestep, 15.87)
        upper_percentile[timestep] = np.percentile(infections_at_timestep, 84.13)
    
    return average_infections, lower_percentile, upper_percentile, total_people


def main():
    """load_results = True
    
    # Generate sim results
    if not load_results:
        sim_results = get_simulation_results(masked=True, repeat_sims=25, save_results=True)
    
    # Load sim results
    if load_results:
        sim_results = load_simulation_results("data/unmasked_25_results.csv")
    
    plot_simulation_results(sim_results, plot_average=False, plot_percentiles=False, plot_simulations=True)"""
    
    # Plot both masked and unmasked results
    sim_results_masked = load_simulation_results("data/masked_25_results.csv")
    sim_results_unmasked = load_simulation_results("data/unmasked_25_results.csv")
    
    # Get average and std for total time taken to infect everyone
    final_infections_masked = [sim_result[-1]["timestep"] for sim_result in sim_results_masked]
    final_infections_unmasked = [sim_result[-1]["timestep"] for sim_result in sim_results_unmasked]
    
    average_final_infections_masked = np.mean(final_infections_masked)
    std_final_infections_masked = np.std(final_infections_masked)
    
    average_final_infections_unmasked = np.mean(final_infections_unmasked)
    std_final_infections_unmasked = np.std(final_infections_unmasked)
    
    print(f"Average time to infect everyone (masked): {average_final_infections_masked} +/- {std_final_infections_masked}")
    print(f"Average time to infect everyone (unmasked): {average_final_infections_unmasked} +/- {std_final_infections_unmasked}")
    
    
    
    plot_average = True
    plot_percentiles = True
    
    average_infections_masked, lower_percentile_masked, upper_percentile_masked, total_people_masked = get_average_and_percentiles(sim_results_masked)
    average_infections_unmasked, lower_percentile_unmasked, upper_percentile_unmasked, total_people_unmasked = get_average_and_percentiles(sim_results_unmasked)
    
    timesteps_masked = np.arange(0, len(average_infections_masked))
    timesteps_unmasked = np.arange(0, len(average_infections_unmasked))
    
    plt.fill_between(timesteps_masked, lower_percentile_masked / total_people_masked * 100, upper_percentile_masked / total_people_masked * 100, alpha=0.3, color='blue', label=r"1 $\sigma$ error on mean (masked)", zorder=2)
    plt.plot(timesteps_masked, average_infections_masked / total_people_masked * 100, label="Mean infections (masked)", color='blue', zorder=3)
    
    plt.fill_between(timesteps_unmasked, lower_percentile_unmasked / total_people_unmasked * 100, upper_percentile_unmasked / total_people_unmasked * 100, alpha=0.3, color='red', label=r"1 $\sigma$ error on mean (unmasked)", zorder=2)
    plt.plot(timesteps_unmasked, average_infections_unmasked / total_people_unmasked * 100, label="Mean infections (unmasked)", color='red', zorder=3)
    
    plt.xlabel("Timestep")
    plt.ylabel("Percentage of people infected (%)")
    plt.legend()
    
    plt.savefig("plots/masked_vs_unmasked_avg.pdf", format='pdf')
    plt.show()
    
        

if __name__ == '__main__':
    main()