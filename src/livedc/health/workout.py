
import pandas as pd
from ..desc import add_rdoc


@add_rdoc
def fat_burning_heart_rate(age):

    """
    The fat-burning zone is typically 70-80% of the maximum heart rate, which is calculated as:
    $$ \\text{Maximum Heart Rate} = 220 - \\text{Age} $$
    The lower and upper bounds of the fat-burning heart rate range are then calculated as:
    $$ \\text{Lower Bound} = \\text{Maximum Heart Rate} \\times 0.7 $$
    $$ \\text{Upper Bound} = \\text{Maximum Heart Rate} \\times 0.8 $$

    Args:
        age (int): Age of the person.
        
    Returns:
        tuple: A tuple containing the lower and upper bounds of the heart rate range.
    
    Reference:
    * [Cracking the Code: Heart Rate Zones for Fat Burning](https://www.miramont.us/blog/heart-rate-to-burn-fat)
    """
    max_heart_rate = 220 - age
    lower_bound = max_heart_rate * 0.7
    upper_bound = max_heart_rate * 0.8
    return lower_bound, upper_bound



if __name__ == "__main__":
  # print (approx_Euler(10))
  # plot_Euler()
  pass
