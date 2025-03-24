from tabulate import tabulate
import matplotlib.pyplot as plt

class Process:
    def init(self, pid, arrival_time, burst_time, priority):
        self.pid = pid
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority
        self.remaining_time = burst_time
        self.completion_time = 0
        self.start_times = []  # Track start times for Gantt chart
        self.end_times = []    # Track end times for Gantt chart

def multilevel_feedback_queue(processes, time_quantum1, time_quantum2, time_quantum3):
    queue1 = []
    queue2 = []
    queue3 = []
    time = 0
    completed_processes = []

    # Sort processes by arrival time
    processes.sort(key=lambda p: p.arrival_time)

    while processes or queue1 or queue2 or queue3:
        # Move processes to queue 1 when they arrive
        while processes and processes[0].arrival_time <= time:
            queue1.append(processes.pop(0))

        # Print state of queues
        print(f"\nTime {time}:")
        print("Queue 1:", [p.pid for p in queue1])
        print("Queue 2:", [p.pid for p in queue2])
        print("Queue 3:", [p.pid for p in queue3])

        if queue1:
            current_process = queue1.pop(0)
            current_process.start_times.append(time)
            execution_time = min(current_process.remaining_time, time_quantum1)
            time += execution_time
            current_process.remaining_time -= execution_time
            current_process.end_times.append(time)

            # Check if the process needs to move to a lower-priority queue
            if current_process.remaining_time > 0:
                if queue1 or queue2 or queue3 or (processes and processes[0].arrival_time <= time):
                    queue2.append(current_process)
                else:
                    queue1.append(current_process)  # Stay in the same queue if no other process is waiting
            else:
                current_process.completion_time = time
                completed_processes.append(current_process)

        elif queue2:
            current_process = queue2.pop(0)
            current_process.start_times.append(time)
            execution_time = min(current_process.remaining_time, time_quantum2)
            time += execution_time
            current_process.remaining_time -= execution_time
            current_process.end_times.append(time)

            # Check if the process needs to move to a lower-priority queue
            if current_process.remaining_time > 0:
                if queue1 or queue2 or queue3 or (processes and processes[0].arrival_time <= time):
                    queue3.append(current_process)
                else:
                    queue2.append(current_process)  # Stay in the same queue if no other process is waiting
            else:
                current_process.completion_time = time
                completed_processes.append(current_process)

        elif queue3:
            current_process = queue3.pop(0)
            current_process.start_times.append(time)
            execution_time = min(current_process.remaining_time, time_quantum3)
            time += execution_time
            current_process.remaining_time -= execution_time
            current_process.end_times.append(time)

            if current_process.remaining_time > 0:
                queue3.append(current_process)  # Stay in queue 3
            else:
                current_process.completion_time = time
                completed_processes.append(current_process)

        elif processes:
            time = processes[0].arrival_time

    # Sort processes by PID for consistent order
    completed_processes.sort(key=lambda p: p.pid)

    # Plot Gantt chart
    fig, ax = plt.subplots(figsize=(12, 6))
    colors = ["skyblue", "salmon", "lightgreen", "orange", "purple"]

    for i, p in enumerate(completed_processes):
        y_position = i  # Correct y-position for each process
        for start, end in zip(p.start_times, p.end_times):
            ax.barh(
                y_position,
                end - start,
                left=start,
                color=colors[i % len(colors)],
                edgecolor="black",
                height=1.0,  # Full height to touch top and bottom lines
            )
        # Add a horizontal line at the top of each process bar
        ax.axhline(y=y_position + 0.5, color="black", linestyle="--", linewidth=0.8)

    # Add horizontal line for x-axis (bottom line)
    ax.axhline(y=-0.5, color="black", linestyle="--", linewidth=0.8)

    # Draw vertical grid lines for every unit on the x-axis
    ax.set_xticks(range(0, time + 1))
    ax.grid(axis='x', linestyle='--', linewidth=0.5, which='both', color="grey")

    # Configure Y-axis to list processes by PID
    ax.set_yticks(range(len(completed_processes)))
    ax.set_yticklabels([f"P{p.pid}" for p in completed_processes])

    ax.set_ylim(-0.5, len(completed_processes) - 0.5)
    ax.set_xlabel("Time (units)")
    ax.set_title("Multilevel Feedback Queue Scheduling (Gantt Chart)")
    plt.tight_layout()
    plt.show()


    # Calculate and display process times
    table = []
    for p in completed_processes:
        tat = p.completion_time - p.arrival_time
        wt = tat - p.burst_time
        table.append([p.pid, p.arrival_time, p.burst_time, p.completion_time, tat, wt])

    headers = ["PID", "Arr", "Burst", "Comp", "TAT", "WT"]
    print("\nFinal Process Times:")
    print(tabulate(table, headers=headers, tablefmt="grid", numalign="center", stralign="center"))

# Accept user input
def get_user_input():
    num_processes = int(input("Enter the number of processes: "))
    processes = []
    for i in range(num_processes):
        print(f"\nEnter details for Process {i + 1}:")
        pid = int(input("PID: "))
        arrival_time = int(input("Arrival Time: "))
        burst_time = int(input("Burst Time: "))
        priority = int(input("Priority (0 for this implementation): "))
        processes.append(Process(pid, arrival_time, burst_time, priority))
    return processes

# Main program
processes = get_user_input()
time_quantum1 = int(input("\nEnter Time Quantum for Queue 1: "))
time_quantum2 = int(input("Enter Time Quantum for Queue 2: "))
time_quantum3 = int(input("Enter Time Quantum for Queue 3: "))

multilevel_feedback_queue(processes, time_quantum1, time_quantum2, time_quantum3)