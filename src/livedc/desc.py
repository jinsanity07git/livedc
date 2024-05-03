from IPython.display import display, Markdown,Math,Latex,TextDisplayObject
from IPython.display import IFrame
from ipywidgets import HBox,HTML,GridBox,Output
import pandas as pd

def preview(iterables):
    for x in iterables: display(x)
    

def add_rdoc(func):
    """Decorator to add a __rdoc__ attribute to a function by parsing and
    converting the __doc__ string with Markdown and IPython.display.
    """
    doc = func.__doc__
    rdoc_sections = []
    for section in doc.split("```"):
        if "md" in section[:10]:
            rdoc_sections.append(Markdown(section[2:].lstrip()))
        elif "txt" in section[:10]:
            # Uncomment the following line to include plain text sections
            # rdoc_sections.append(Markdown(section[3:]) )
            pass
        else:
            # backslah handler for latex symbol in string
            if "\x0crac" in section:
                section = section.replace("\x0crac","\\frac")
            rdoc_sections.append(Markdown(section.lstrip()))
    # func.__rdoc__ = "\n".join([str(section) for section in rdoc_sections])
    func.__rdoc__ = rdoc_sections
    func.rdoc = lambda: preview(func.__rdoc__)
    return func


def sbs( iter ):
    """
    sbs([dfmat.iloc[:,:1],dfmat.iloc[:,:2]])

    Args:
        iter (_type_): _description_

    Returns:
        _type_: _description_
        
    """
    ls = []
    for df in iter:
        if isinstance(df, pd.Series):
            df = pd.DataFrame(df)
        ls.append(  HTML(df.to_html())  )
    return (HBox(ls))
