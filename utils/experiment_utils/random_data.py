import random
from collections.abc import Callable


# Note: 120 total items because it is a very divisible number (2, 3, 4, 5, 6, 8, 10, 12...)
def get_data(
    num_best_items: int = 20,
    num_total_items: int = 120,
    format_team_data: Callable[[str, bool], dict] = lambda x: {},
) -> tuple[dict[str, dict], list[str]]:
    """
    Given the number of best items, and total number of items, generate two things:

    1. A dict where the keys are the item's identifier (basically a unique index), and the team's data, as determined by format_team_data().
    2. A list consisting of the keys of the best items.

    format_team_data() takes data of the team, and formats the data as a dictionary.
    """

    # Simple check that values make sense.
    assert (
        num_best_items < num_total_items
    ), f"num_total_items, {num_total_items} is less than num_best_items {num_best_items}"

    # Team names are keys
    all_items = {str(key): {} for key in range(num_total_items)}

    # Keys of the best items, chosen at random
    best_items = random.sample(range(num_total_items), k=num_best_items)
    best_items = [str(item) for item in best_items]

    for key in all_items.keys():
        if key in best_items:
            all_items[key] = format_team_data(key, True)
        else:
            all_items[key] = format_team_data(key, False)

    return all_items, best_items
