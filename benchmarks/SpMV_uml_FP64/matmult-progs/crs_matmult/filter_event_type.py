import json

# Load the uploaded JSON file
file_path = "list_of_all_hw_events.json"
with open(file_path, "r") as f:
    events_data = json.load(f)

# Filter for EventType == "Kernel PMU event" or "Hardware cache event"
filtered_events = [
    event for event in events_data
    if event.get("EventType") in ["Kernel PMU event", "Hardware cache event"]
]

# Save filtered results
filtered_file_path = "filtered_kernelpmu_hwcache_events.json"
with open(filtered_file_path, "w") as f:
    json.dump(filtered_events, f, indent=4)

(len(filtered_events), filtered_file_path)
