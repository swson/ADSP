#!/usr/bin/env python3
import json

# Load the provided JSON file
input_path = 'list_of_all_hw_events.json'
output_path = 'filtered_events.json'

with open(input_path, 'r') as f:
    events = json.load(f)

# Filter out events without EventType
filtered_events = [event for event in events if event.get("EventType")]

# Save filtered events to a new file
with open(output_path, 'w') as f:
    json.dump(filtered_events, f, indent=4)

# Count the number of filtered events
filtered_count = len(filtered_events)

filtered_count, output_path
