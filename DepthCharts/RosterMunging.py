import pandas as pd
import re

def filter_csv(input_file, output_file, valid_pos):
    """Removes items from columns that don't match an element

    Using to filter only positions I want

    Args:
        input_file (String): _description_
        output_file (String): _description_
        valid_pos (List of strings): _description_

    
    """

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)

    # Filter the DataFrame to keep only rows where 'POS' matches any string in valid_pos
    filtered_df = df[df['Pos'].isin(valid_pos)]

    # Remove consecutive duplicates
    filtered_df = filtered_df[filtered_df['Pos'].shift() != filtered_df['Pos']]

    # Save the filtered DataFrame back to a CSV file
    filtered_df.to_csv(output_file, index=False)

def clean_csv(input_file, output_file, cols):
    """Cleaning the names used in my csvs to non-name info and format as 'first last' instead of 'last, first'

    Args:
        input_file (_type_): _description_
        output_file (_type_): _description_
        cols (List of String): Columns to run filter over
    """

    # Read the CSV file into a DataFrame
    df = pd.read_csv(input_file)
    
    for column in cols:
        df[column] = df[column].apply(lambda item:
                                        clean_and_format_name(item)
                                        if isinstance(item, str)
                                        else item
                                        )
    df = df.drop(columns=['No','No.1','No.2','No.3','No.4',])
    df.to_csv(output_file, index=False)

def merge_csv(wr_file, input_file):
    """Specific use file that merges wide receiver file with rest of dataset

    Args:
        wr_file (_type_): _description_
        input_file (_type_): _description_
    """
    df = pd.read_csv(wr_file)
    df = df.drop(columns=['INJURED RESERVE'])
    wr_cols = ['WR1','WR2','WR3']

    for column in wr_cols:
        df[column] = df[column].apply(lambda item:
                                      re.sub(r'\(R\)', '',item).strip()
                                      )

    df = df.rename(columns={'TEAMS': 'Team', 'WR1': 'Player 1','WR2': 'Player 2','WR3': 'Player 3'})
    df = df.assign(Pos = 'WR')

    rdf = pd.read_csv(input_file)
    rdf = pd.concat([rdf,df], axis=0)
    rdf = rdf.sort_values(by='Team')
    rdf.to_csv(input_file, index=False)

def clean_and_format_name(name):
    """Cleans data and arranges in an acceptable format

    Args:
        name (String): String to clean and format

    Returns:
        String: Cleaned and formatted string
    """
    # Remove extra info and split into last and first name
    cleaned = re.sub(r'(.*?,\s*\S+).*', r'\1', name)
    last, first = cleaned.split(',')
    
    # Capitalize first letter of each name and swap order
    formatted = f"{first.strip().capitalize()} {last.strip().capitalize()}"
    
    return formatted

# Example usage
input_file = 'depthchart.csv'
output_file = 'OFFdepthchart.csv'
wr_file = 'WRDepthCharts.csv'
valid_pos = ['TE', 'RB', 'QB']  # List of valid POS tags
cols = ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Player 5']

filter_csv(input_file, output_file, valid_pos)
clean_csv(output_file, output_file, cols)
merge_csv(wr_file, output_file)