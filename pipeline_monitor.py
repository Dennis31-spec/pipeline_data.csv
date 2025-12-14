import csv
from collections import defaultdict

# --- 1. Core Sales Metrics Calculations ---

def analyze_pipeline(data):
    # Initialize variables for key metrics
    stage_counts = defaultdict(int)
    stage_time_sum = defaultdict(int)
    total_active_value = 0
    total_closed_won = 0
    total_closed_lost = 0
    
    active_stages = set(['Discovery', 'Proposal', 'Negotiation'])

    for deal in data:
        stage = deal['Stage']
        amount = int(deal['Amount'])
        days = int(deal['Stage_Days'])
        
        # Aggregate counts and time spent per stage
        stage_counts[stage] += 1
        stage_time_sum[stage] += days
        
        if stage in active_stages:
            total_active_value += amount
        elif stage == 'Closed Won':
            total_closed_won += amount
        elif stage == 'Closed Lost':
            total_closed_lost += amount

    # --- 2. Calculate Derived Metrics ---
    
    report = {
        "Total Active Pipeline Value": f"${total_active_value:,}",
        "Total Closed Won Value": f"${total_closed_won:,}",
        "Total Closed Lost Value": f"${total_closed_lost:,}",
        "Average Deal Size (Won/Lost)": f"${(total_closed_won + total_closed_lost) / (stage_counts['Closed Won'] + stage_counts['Closed Lost']):,.2f}" if (stage_counts['Closed Won'] + stage_counts['Closed Lost']) else "N/A",
        "\n--- Stage Health Report ---": "",
    }
    
    # Calculate Average Time in Stage (Velocity) and identify potential bottlenecks
    for stage in active_stages:
        if stage_counts[stage] > 0:
            avg_time = stage_time_sum[stage] / stage_counts[stage]
            status = "✅ Healthy"
            if avg_time > 20: # Example threshold for a bottleneck
                 status = "⚠️ BOTTLENECK: High Average Days"
            
            report[f"Avg Days in {stage}"] = f"{avg_time:.1f} days ({stage_counts[stage]} deals) {status}"

    return report

# --- 3. Main Execution ---

def run_monitor():
    print("--- Sales Pipeline Health Monitor V1.0 ---")
    
    try:
        # Load the simulated pipeline data from CSV
        with open('pipeline_data.csv', mode='r') as file:
            reader = csv.DictReader(file)
            data = list(reader)
    except FileNotFoundError:
        print("Error: pipeline_data.csv not found.")
        return

    analysis_results = analyze_pipeline(data)

    print("\n📊 Key Performance Indicators (KPIs):\n")
    # Print results in a formatted way
    max_key_length = max(len(key) for key in analysis_results.keys())
    for key, value in analysis_results.items():
        if key.startswith("---"):
            print(f"\n{key}")
        else:
            print(f"{key:<{max_key_length}}: {value}")

if __name__ == '__main__':
    run_monitor()
