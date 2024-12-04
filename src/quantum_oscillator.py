import numpy as np
import math
from plotly.subplots import make_subplots
import plotly.graph_objects as go
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Constants
N_POINTS = 1000
RANGE_FACTOR = 1.2  # Factor to extend beyond classical turning points

def hermite(n, x):
    """Calculate the nth Hermite polynomial at points x."""
    if n == 0:
        return np.ones_like(x)
    elif n == 1:
        return 2 * x
    else:
        h_prev = np.ones_like(x)  # H_0
        h_curr = 2 * x            # H_1
        
        for i in range(2, n + 1):
            h_next = 2 * x * h_curr - 2 * (i - 1) * h_prev
            h_prev = h_curr
            h_curr = h_next
        
        return h_curr

def wavefunction(n, x):
    """Calculate the nth wavefunction."""
    # Using normalized units where ℏ = m = ω = 1
    xi = x  # In normalized units, ξ = sqrt(mω/ℏ) x = x
    normalization = 1.0 / np.sqrt(2**n * math.factorial(n) * np.sqrt(np.pi))
    return normalization * hermite(n, xi) * np.exp(-xi**2 / 2)

def classical_distribution(n, x):
    """Calculate the classical position distribution for nth state."""
    # Using normalized units where ℏ = m = ω = 1
    energy = n + 1/2  # Classical energy in normalized units
    result = np.zeros_like(x)
    # Calculate only where expression under sqrt is positive
    mask = x**2 < energy*2
    result[mask] = 1 / (np.pi * np.sqrt(energy*2 - x[mask]**2))
    return result

def check_normalization(x, prob):
    """Check the normalization of a probability distribution using numerical integration."""
    integral = np.trapz(prob, x)
    return integral

def get_x_range(n):
    """Calculate the x-axis range based on classical turning points."""
    # Classical turning points at ±√(2n + 1) in normalized units
    turning_point = np.sqrt(2 * n + 1)
    x_max = RANGE_FACTOR * turning_point
    return -x_max, x_max

def get_y_max(probability):
    """Calculate the maximum value between quantum and classical probability densities."""
    return np.max(probability)

# Create Dash app
app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Quantum Harmonic Oscillator: Probability Density',
            style={'text-align': 'center'}),
    html.Div([
        html.Label('Energy Level n:'),
        dcc.Slider(
            id='n-slider',
            min=0,
            max=100,
            value=0,
            marks={i: str(i) for i in range(0, 101, 10)},
            step=1
        )
    ], style={'width': '80%', 'margin': 'auto', 'padding': '20px'}),
    dcc.Graph(id='wavefunction-plot')
])

@app.callback(
    Output('wavefunction-plot', 'figure'),
    [Input('n-slider', 'value')]
)
def update_figure(n):
    xmin, xmax = get_x_range(n)
    x = np.linspace(xmin, xmax, N_POINTS)
    
    # Calculate and verify quantum probability
    psi = wavefunction(n, x)
    probability = np.abs(psi)**2
    quantum_norm = check_normalization(x, probability)
    if abs(quantum_norm - 1.0) > 0.01:  # Allow 1% error
        print(f"Warning: Quantum probability not normalized. Integral = {quantum_norm}")
    
    # Calculate and verify classical probability
    classical_prob = classical_distribution(n, x)
    classical_norm = check_normalization(x, classical_prob)
    if abs(classical_norm - 1.0) > 0.01:  # Allow 1% error
        print(f"Warning: Classical probability not normalized. Integral = {classical_norm}")
        classical_prob = classical_prob / classical_norm  # Normalize if needed
    
    # Calculate y-axis range
    y_max = get_y_max(probability)
    y_range_max = y_max * RANGE_FACTOR  # Use same factor as x-axis
    
    fig = make_subplots(rows=1, cols=1)
    
    # Quantum probability density
    fig.add_trace(
        go.Scatter(x=x, y=probability, mode='lines', name='Quantum |ψₙ(x)|²',
                  line=dict(color='blue', width=2))
    )
    
    # Classical position distribution
    fig.add_trace(
        go.Scatter(x=x, y=classical_prob, mode='lines', name='Classical ρₙ(x)',
                  line=dict(color='red', width=2, dash='dot'))
    )
    
    # Add vertical lines at classical turning points
    turning_point = np.sqrt(2 * n + 1)
    for tp in [-turning_point, turning_point]:
        fig.add_vline(x=tp, line_dash="dash", line_color="gray", opacity=0.5,
                     annotation_text="Classical turning point")
    
    fig.update_layout(
        title=f'Quantum vs Classical Probability Distribution for n = {n}',
        xaxis_title='Position (x)',
        yaxis_title='Probability Density',
        showlegend=True,
        hovermode='x',
        plot_bgcolor='white',
        yaxis=dict(range=[0, y_range_max])
    )
    
    fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='LightGray',
                    showticklabels=False)  # Hide x-axis numeric values
    fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='LightGray')
    
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
