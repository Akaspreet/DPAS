import matplotlib.pyplot as plt
import seaborn as sns

def analyze_property_type_change(df):
    # Implement analysis logic here
    # Generate and save graph
    plt.figure(figsize=(12, 6))
    # Plot logic here
    plt.savefig('static/graphs/property_type_change.png')
    plt.close()
    return 'static/graphs/property_type_change.png'

# Implement other analysis functions as needed