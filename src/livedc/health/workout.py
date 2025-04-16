
import pandas as pd
from ..desc import add_rdoc


@add_rdoc
def fat_burning_heart_rate(age):

    """
    The fat-burning zone is typically 50-70% of the maximum heart rate, which is calculated as:
    $$ \\text{Maximum Heart Rate} = 220 - \\text{Age} $$
    The lower and upper bounds of the fat-burning heart rate range are then calculated as:
    $$ \\text{Lower Bound} = \\text{Maximum Heart Rate} \\times 0.5 $$
    $$ \\text{Upper Bound} = \\text{Maximum Heart Rate} \\times 0.7 $$

    Args:
        age (int): Age of the person.
        
    Returns:
        tuple: A tuple containing the lower and upper bounds of the heart rate range.
    """
    max_heart_rate = 220 - age
    lower_bound = max_heart_rate * 0.5
    upper_bound = max_heart_rate * 0.7
    return lower_bound, upper_bound



if __name__ == "__main__":
  # print (approx_Euler(10))
  # plot_Euler()
  pass
