import csv

def read_inventory():
    inventory = []
    try:
        with open("stock.csv", "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                if row:
                    inventory.append(row)
    except FileNotFoundError:
        print("stock.csv file not founded")
    return inventory

def check_inventory(inventory):
    processed = []
    for item in inventory:
        try:
            name = item["Item"]
            current_str = item["Current Quantity"]
            threshold_str = item["Threshold"]
            
            if name == "" or current_str == "" or threshold_str == "":
                continue
                
            current = int(current_str)
            threshold = int(threshold_str)
            
            status = "In Stock"
            priority = ""
            reorder = 0
            
            if current < threshold:
                status = "Restock Needed"
                if current <= (threshold * 0.25):
                    priority = "Critical"
                else:
                    priority = "Low"
                    
                reorder = (threshold * 2) - current
                if reorder < 0:
                    reorder = 0
            
            new_item = {
                "Item": name,
                "Current Quantity": current,
                "Threshold": threshold,
                "Status": status,
                "Priority": priority,
                "Suggested Reorder Quantity": reorder
            }
            
            processed.append(new_item)
        except ValueError:
            continue
        except KeyError:
            continue
            
    return processed

def print_report(inventory):
    print("Inventory Report")
    print("-" * 80)
    for item in inventory:
        name = item["Item"]
        current = item["Current Quantity"]
        threshold = item["Threshold"]
        status = item["Status"]
        priority = item["Priority"]
        reorder = item["Suggested Reorder Quantity"]
        
        line = f"{name} | Current: {current} | Threshold: {threshold} | Status: {status}"
        if priority != "":
            line += f" | Priority: {priority} | Reorder: {reorder}"
            
        print(line)
    print("-" * 80)

def export_report(inventory):
    try:
        with open("restock_report.csv", "w", newline="") as file:
            fields = ["Item", "Current Quantity", "Threshold", "Status", "Priority", "Suggested Reorder Quantity"]
            writer = csv.DictWriter(file, fieldnames=fields)
            
            writer.writeheader()
            for item in inventory:
                if item["Status"] == "Restock Needed":
                    writer.writerow(item)
    except IOError:
        pass

data = read_inventory()
checked_data = check_inventory(data)
print_report(checked_data)
export_report(checked_data)
print("\nRestock report generated successfully.")