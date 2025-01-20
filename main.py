import csv
import curses
import time


# Function to load filament data from a CSV file
def load_filament_data(file_path):
    """Load filament data from a CSV file."""
    filament_list = []
    try:
        with open(file_path, mode='r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                filament_list.append({
                    "type": row["type"],
                    "color": row["color"],
                    "weight_g": float(row["weight_g"]),
                    "cost_total": float(row["cost_total"]),
                })
    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
        exit()
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        exit()
    return filament_list


# Function to display a selector using curses
def display_selector(stdscr, options, title):
    """Display a selection menu using arrow keys."""
    curses.curs_set(0)
    current_row = 0

    while True:
        stdscr.clear()
        stdscr.addstr(0, 0, title, curses.A_BOLD)
        for idx, option in enumerate(options):
            if idx == current_row:
                stdscr.addstr(idx + 1, 0, option, curses.color_pair(1))
            else:
                stdscr.addstr(idx + 1, 0, option)
        stdscr.refresh()

        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
        elif key == curses.KEY_DOWN and current_row < len(options) - 1:
            current_row += 1
        elif key == ord("\n"):  # Enter key
            return current_row


# Function to select material and color
def select_filament(filament_list):
    """Select filament type and color using arrow keys."""
    def run_selector(stdscr):
        curses.start_color()
        curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_WHITE)
        options = [
            f"{f['type']} ({f['color']}) - {f['weight_g']}g for £{f['cost_total']:.2f}"
            for f in filament_list
        ]
        selected_index = display_selector(stdscr, options, "Select Filament (Arrow Keys + Enter):")
        return selected_index

    return curses.wrapper(run_selector)


# Function to calculate print cost
def calculate_print_cost(filament_data, print_weight_g, profit_margin):
    """Calculate the cost of a print including profit margin."""
    # Calculate material cost per gram dynamically
    material_cost_per_g = filament_data["cost_total"] / filament_data["weight_g"]
    material_cost = material_cost_per_g * print_weight_g

    setup_cost = float(input("Enter fixed setup cost (£) (e.g., £3-£5 for small prints): "))
    operational_cost = float(input("Enter additional operational cost (£): "))

    total_base_cost = material_cost + setup_cost + operational_cost
    profit = total_base_cost * (profit_margin / 100)
    final_price = total_base_cost + profit

    return {
        "material_cost": material_cost,
        "setup_cost": setup_cost,
        "operational_cost": operational_cost,
        "total_base_cost": total_base_cost,
        "profit": profit,
        "final_price": final_price,
    }


# Main program
def main():
    print("--- Advanced 3D Printing Pricing Calculator ---")

    # Load filament data
    file_path = "filament_data.csv"
    filament_list = load_filament_data(file_path)

    # Select filament
    print("Loading filament selector...")
    selected_index = select_filament(filament_list)
    selected_filament = filament_list[selected_index]
    print(
        f"Selected Filament: {selected_filament['type']} ({selected_filament['color']}) - "
        f"{selected_filament['weight_g']}g for £{selected_filament['cost_total']:.2f}"
    )

    # Input print weight and profit margin
    print_weight_g = float(input("Enter print weight (grams): "))
    profit_margin = float(input("Enter desired profit margin (%): "))

    # Calculate costs
    cost_data = calculate_print_cost(selected_filament, print_weight_g, profit_margin)

    # Display results
    print("\n--- Pricing Breakdown ---")
    print(f"Filament Type: {selected_filament['type']}")
    print(f"Filament Color: {selected_filament['color']}")
    print(f"Material Cost: £{cost_data['material_cost']:.2f}")
    print(f"Setup Cost: £{cost_data['setup_cost']:.2f}")
    print(f"Operational Cost: £{cost_data['operational_cost']:.2f}")
    print(f"Total Base Cost: £{cost_data['total_base_cost']:.2f}")
    print(f"Profit: £{cost_data['profit']:.2f}")
    print(f"Final Price to Charge: £{cost_data['final_price']:.2f}")
    time.sleep(3600)


if __name__ == "__main__":
    main()

