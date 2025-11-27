"""Linear programming example with PuLP"""

import pulp


# Resource constraints (units)
WATER_AVAILABLE = 100
SUGAR_AVAILABLE = 50
LEMON_JUICE_AVAILABLE = 30
FRUIT_PUREE_AVAILABLE = 40

# Resource requirements per unit
WATER_PER_LEMONADE = 2
SUGAR_PER_LEMONADE = 1
LEMON_JUICE_PER_LEMONADE = 1
FRUIT_PUREE_PER_LEMONADE = 0
WATER_PER_JUICE = 1
SUGAR_PER_JUICE = 0
FRUIT_PUREE_PER_JUICE = 2
LEMON_JUICE_PER_JUICE = 0


def production_optimization():
    """
    Solve production optimization problem using linear programming.
    The problem is to maximize the total production of lemonade and juice,
    subject to the resource constraints.
    Returns:
        dict: Solution containing juice amount, lemonade amount, total,
              and solver status
    """
    # Create the model
    model = pulp.LpProblem("Maximize_Production", pulp.LpMaximize)

    # Decision variables
    juice = pulp.LpVariable(
        'Juice',
        lowBound=0,
        cat='Integer'
    )
    lemonade = pulp.LpVariable(
        'Lemonade',
        lowBound=0,
        cat='Integer'
    )

    # Objective function
    model += juice + lemonade, "Total_Products"

    # Constraints
    model += (
        WATER_PER_JUICE * juice + WATER_PER_LEMONADE * lemonade
        <= WATER_AVAILABLE
    ), "Water_Constraint"

    model += (
        SUGAR_PER_JUICE * juice + SUGAR_PER_LEMONADE * lemonade
        <= SUGAR_AVAILABLE
    ), "Sugar_Constraint"

    model += (
        LEMON_JUICE_PER_JUICE * juice + LEMON_JUICE_PER_LEMONADE * lemonade
        <= LEMON_JUICE_AVAILABLE
    ), "Lemon_Juice_Constraint"

    model += (
        FRUIT_PUREE_PER_JUICE * juice + FRUIT_PUREE_PER_LEMONADE * lemonade
        <= FRUIT_PUREE_AVAILABLE
    ), "Fruit_Puree_Constraint"

    # Solve the problem
    status = model.solve()

    # Prepare results
    result = {
        'status': pulp.LpStatus[status],
        'juice': juice.varValue if juice.varValue is not None else 0,
        'lemonade': lemonade.varValue if lemonade.varValue is not None else 0
    }

    return result


def print_results(result):
    """
    Print optimization results in a readable format.
    Args:
        result (dict): Dictionary containing optimization results
    """
    print("="*50)
    print("PRODUCTION OPTIMIZATION RESULTS")
    print("="*50)
    print(f"Solver Status: {result['status']}")

    if result['status'] == 'Optimal':
        print(f"\nOptimal Solution Found:")
        print(f"  Juice Production:    {result['juice']:.0f} units")
        print(f"  Lemonade Production: {result['lemonade']:.0f} units")

        # Resource utilization
        water_used = (WATER_PER_JUICE * result['juice'] +
                      WATER_PER_LEMONADE * result['lemonade'])
        sugar_used = (SUGAR_PER_JUICE * result['juice'] +
                      SUGAR_PER_LEMONADE * result['lemonade'])
        lemon_juice_used = (LEMON_JUICE_PER_JUICE * result['juice'] +
                      LEMON_JUICE_PER_LEMONADE * result['lemonade'])
        fruit_puree_used = (FRUIT_PUREE_PER_JUICE * result['juice'] +
                      FRUIT_PUREE_PER_LEMONADE * result['lemonade'])

        print("\nResource Utilization:")
        print(f"  Water: {water_used:.0f}/{WATER_AVAILABLE} units "
              f"({water_used/WATER_AVAILABLE*100:.1f}%)")
        print(f"  Sugar: {sugar_used:.0f}/{SUGAR_AVAILABLE} units "
              f"({sugar_used/SUGAR_AVAILABLE*100:.1f}%)")
        print(f"  Lemon Juice: {lemon_juice_used:.0f}/{LEMON_JUICE_AVAILABLE} units "
              f"({lemon_juice_used/LEMON_JUICE_AVAILABLE*100:.1f}%)")
        print(f"  Fruit Puree: {fruit_puree_used:.0f}/{FRUIT_PUREE_AVAILABLE} units "
              f"({fruit_puree_used/FRUIT_PUREE_AVAILABLE*100:.1f}%)")
    else:
        print("\nNo optimal solution found!")
    print("="*50)


def main():
    """Main execution function."""
    result = production_optimization()
    print_results(result)


if __name__ == "__main__":
    main()
