import matplotlib.pyplot as plt
import io
import base64
import pandas as pd

def extract_and_execute_code(code, df):
    # Create a local environment with necessary imports and the DataFrame
    local_env = {
        'pd': pd,
        'plt': plt,
        'df': df
    }
    
    try:
        # Execute the code
        exec(code, local_env)
        
        # Capture the plot
        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_base64 = base64.b64encode(buffer.getvalue()).decode()
        plt.close()  # Clear the current plot
        
        return {
            'success': True,
            'plot': plot_base64,
            'output': local_env.get('output', '')  # Capture any output variable if defined in the code
        }
    except Exception as e:
        return {
            'success': False,
            'error': str(e)
        }