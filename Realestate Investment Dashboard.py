#Group 44 acknowledges the use of a large language model (LLM) to enhance the visual layout for our code on the 26th of October 2024. A prompt was given to the model stating 'How can you help me ensure these visualisations can be depicted in a better user friendly manner while ensuring engagement'

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np
from datetime import datetime


COLORS = {
    'primary': '#2196F3',
    'secondary': '#4CAF50',
    'accent': '#FFA726',
    'danger': '#F44336',
    'success': '#4CAF50',
    'warning': '#FFA726',
    'background': '#F5F7FA',
    'white': '#FFFFFF',
    'text': '#2C3E50',
    'light_text': '#90A4AE',
    'border': '#E0E6ED',
    'chart_colors': ['#2196F3', '#4CAF50', '#FFA726', '#F44336', '#9C27B0']
}


df = pd.read_csv('investment_property_expenses.csv')
df['Date'] = pd.to_datetime(df['Date'])
df['Year'] = df['Date'].dt.year
df['Month'] = df['Date'].dt.month
df['YearMonth'] = df['Date'].dt.strftime('%Y-%m')
df['Quarter'] = df['Date'].dt.quarter
df['YearQuarter'] = df['Date'].dt.year.astype(str) + '-Q' + df['Date'].dt.quarter.astype(str)

# Calculate additional metrics
df['Gross_Income'] = df['Rent_Received'] + df['Additional_Income']
df['Operating_Expenses'] = (df['Property_Management_Fees'] + df['Utilities'] + 
                          df['Strata_Fees'] + df['Routine_Maintenance'] + 
                          df['Council_Rates'] + df['Other_Miscellaneous_Costs'])
df['NOI'] = df['Gross_Income'] - df['Operating_Expenses']
df['Total_Income'] = df['Rent_Received'] + df['Additional_Income']
df['Total_Expenses'] = (df['Property_Management_Fees'] + df['Utilities'] + 
                       df['Strata_Fees'] + df['Routine_Maintenance'] + 
                       df['Council_Rates'])

# Prepare property data
property_data = df[['Location', 'Property_Type']].drop_duplicates().reset_index(drop=True)
property_data['Property'] = property_data['Location'] + ' ' + property_data['Property_Type']
property_data['Latitude'] = [-33.8915, -33.9005, -33.9200]
property_data['Longitude'] = [151.2767, 151.2633, 151.2586]

app = dash.Dash(__name__, suppress_callback_exceptions=True)

# Custom CSS
app.index_string = '''
<!DOCTYPE html>
<html>
    <head>
        {%metas%}
        <title>Property Investment Dashboard</title>
        {%favicon%}
        {%css%}
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&display=swap');
            
            body {
                font-family: 'Inter', sans-serif;
                margin: 0;
                background-color: #F5F7FA;
            }
            
            .dash-dropdown .Select-control {
                height: 38px;
                border-radius: 6px;
                border: 1px solid #E0E6ED;
            }
            
            .dash-dropdown .Select-control:hover {
                border-color: #2196F3;
            }
            
            .input-container {
                position: relative;
                margin-bottom: 15px;
            }
            
            .input-container label {
                display: block;
                margin-bottom: 5px;
                color: #2C3E50;
                font-weight: 500;
            }
            
            .input-container input {
                width: 100%;
                height: 38px;
                padding: 8px 12px;
                border: 1px solid #E0E6ED;
                border-radius: 6px;
                font-size: 14px;
            }
            
            .tab-container {
                margin-bottom: 20px;
            }
            
            .tab-selected {
                border-bottom: 2px solid #2196F3;
                color: #2196F3;
            }
            
            .chart-container {
                background-color: white;
                border-radius: 8px;
                padding: 20px;
                margin-bottom: 20px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
            }

            .chart-title {
                font-size: 18px;
                font-weight: 500;
                color: #2C3E50;
                margin-bottom: 15px;
            }
            
            .metric-label {
                font-size: 14px;
                color: #90A4AE;
                margin-bottom: 5px;
            }
            
            .metric-value {
                font-size: 24px;
                font-weight: 600;
                color: #2196F3;
            }
            
            .metric-card {
                background: white;
                border-radius: 8px;
                padding: 15px;
                box-shadow: 0 1px 3px rgba(0,0,0,0.1);
                flex: 1;
                margin: 0 10px;
            }
        </style>
    </head>
    <body>
        {%app_entry%}
        <footer>
            {%config%}
            {%scripts%}
            {%renderer%}
        </footer>
    </body>
</html>
'''

# Main Layout
app.layout = html.Div([
    # Header
    html.Div([
        html.H1(
            'Investment Property Dashboard', 
            style={
                'color': COLORS['white'],
                'margin': '0',
                'fontSize': '24px',
                'fontWeight': '500'
            }
        ),
        html.Div([
            html.Span(
                "Welcome, Mr. Thomas", 
                style={
                    'fontWeight': '500',
                    'color': COLORS['white']
                }
            ),
            html.Div(
                "Logged in", 
                style={
                    'fontSize': '12px',
                    'color': COLORS['white'],
                    'opacity': '0.8'
                }
            )
        ], style={'textAlign': 'right'})
    ], style={
        'backgroundColor': COLORS['primary'],
        'padding': '15px 25px',
        'display': 'flex',
        'justifyContent': 'space-between',
        'alignItems': 'center',
        'boxShadow': '0 2px 4px rgba(0,0,0,0.1)'
    }),

# Main Content Container
    html.Div([
        # Left Sidebar
        html.Div([
            # Map Container
            html.Div([
                html.H3(
                    "Property Locations", 
                    style={
                        'margin': '0 0 15px 0',
                        'fontSize': '16px',
                        'fontWeight': '500',
                        'color': COLORS['text']
                    }
                ),
                dcc.Graph(
                    id='property-map',
                    style={
                        'height': '200px',
                        'margin': '0'
                    }
                )
            ], className='chart-container'),

            # Controls Container
            html.Div([
                # Property Selection
                html.Div([
                    html.Label(
                        'Select Properties:', 
                        style={
                            'fontWeight': '500',
                            'color': COLORS['text'],
                            'marginBottom': '5px',
                            'display': 'block'
                        }
                    ),
                    dcc.Dropdown(
                        id='property-dropdown',
                        options=[
                            {'label': f"{loc} {type_}", 'value': loc} 
                            for loc, type_ in df[['Location', 'Property_Type']].drop_duplicates().values
                        ],
                        value=[df['Location'].iloc[0]],
                        multi=True,
                        style={'marginBottom': '15px'}
                    )
                ], className='input-container'),

                # Time Period Selection (Monthly only)
                html.Div([
                    html.Label(
                        'Time Period:', 
                        style={
                            'fontWeight': '500',
                            'color': COLORS['text'],
                            'marginBottom': '5px',
                            'display': 'block'
                        }
                    ),
                    dcc.Dropdown(
                        id='time-format',
                        options=[
                            {'label': 'Monthly', 'value': 'month'}
                        ],
                        value='month',
                        style={'marginBottom': '15px'}
                    )
                ], className='input-container'),

                # Financial Details Section
                html.H4(
                    'Property Financial Details:', 
                    style={
                        'margin': '20px 0 15px 0',
                        'fontSize': '16px',
                        'fontWeight': '500',
                        'color': COLORS['text']
                    }
                ),
                
                # Purchase Price Input
                html.Div([
                    html.Label('Purchase Price:', style={'marginBottom': '5px'}),
                    html.Div([
                        html.Span(
                            '$', 
                            style={
                                'position': 'absolute',
                                'left': '10px',
                                'top': '50%',
                                'transform': 'translateY(-50%)',
                                'color': COLORS['light_text']
                            }
                        ),
                        dcc.Input(
                            id='purchase-price',
                            type='number',
                            value=1000000,
                            style={
                                'paddingLeft': '25px',
                                'width': 'calc(100% - 25px)'
                            }
                        )
                    ], style={'position': 'relative'})
                ], className='input-container'),

                # Down Payment Input
                html.Div([
                    html.Label('Down Payment:', style={'marginBottom': '5px'}),
                    html.Div([
                        html.Span(
                            '$', 
                            style={
                                'position': 'absolute',
                                'left': '10px',
                                'top': '50%',
                                'transform': 'translateY(-50%)',
                                'color': COLORS['light_text']
                            }
                        ),
                        dcc.Input(
                            id='down-payment',
                            type='number',
                            value=100000,
                            style={
                                'paddingLeft': '25px',
                                'width': 'calc(100% - 25px)'
                            }
                        )
                    ], style={'position': 'relative'})
                ], className='input-container'),

                # Interest Rate Input
                html.Div([
                    html.Label('Interest Rate:', style={'marginBottom': '5px'}),
                    html.Div([
                        dcc.Input(
                            id='interest-rate',
                            type='number',
                            value=3.5,
                            style={
                                'paddingRight': '30px',
                                'width': 'calc(100% - 30px)'
                            }
                        ),
                        html.Span(
                            '%', 
                            style={
                                'position': 'absolute',
                                'right': '10px',
                                'top': '50%',
                                'transform': 'translateY(-50%)',
                                'color': COLORS['light_text']
                            }
                        )
                    ], style={'position': 'relative'})
                ], className='input-container'),

                # Update Button
                html.Button(
                    'Update Analysis',
                    id='update-button',
                    style={
                        'width': '100%',
                        'backgroundColor': COLORS['primary'],
                        'color': COLORS['white'],
                        'border': 'none',
                        'borderRadius': '6px',
                        'padding': '10px',
                        'fontSize': '14px',
                        'fontWeight': '500',
                        'cursor': 'pointer',
                        'transition': 'background-color 0.2s',
                        'marginTop': '10px'
                    }
                )
            ], className='chart-container')
        ], style={
            'width': '300px',
            'marginRight': '20px',
            'flex': 'none'
        }),

        # Right Content Area with Tabs
        html.Div([
            dcc.Tabs(
                id='tabs',
                value='tab-1',
                className='tab-container',
                children=[
                    dcc.Tab(
                        label='Overview',
                        value='tab-1',
                        className='custom-tab',
                        selected_className='tab-selected'
                    ),
                    dcc.Tab(
                        label='Expense Analysis',
                        value='tab-2',
                        className='custom-tab',
                        selected_className='tab-selected'
                    ),
                    dcc.Tab(
                        label='Financial Forecasting',
                        value='tab-4',
                        className='custom-tab',
                        selected_className='tab-selected'
                    )
                ],
                style={
                    'borderBottom': f'1px solid {COLORS["border"]}',
                    'marginBottom': '20px'
                }
            ),
            # Tab Content Container
            html.Div(
                id='tab-content',
                style={'minHeight': '600px'}
            )
        ], style={'flex': '1'})
    ], style={
        'display': 'flex',
        'padding': '20px',
        'minHeight': 'calc(100vh - 64px)',
        'backgroundColor': COLORS['background']
    })
])

# Visualization Functions
def create_roi_gauge(df, properties, purchase_price, down_payment):
    """Create ROI gauge visualization with improved text"""
    filtered_df = df[df['Location'].isin(properties)]
    monthly_income = filtered_df['Net_Income'].mean()
    annual_income = monthly_income * 12
    
    # Calculate ROI
    total_investment = down_payment + (purchase_price * 0.04)
    roi = (annual_income / total_investment) * 100
    
    fig = go.Figure()
    
    # Add gauge with improved title and formatting
    fig.add_trace(go.Indicator(
        mode="gauge+number",
        value=roi,
        number={'suffix': '%', 'font': {'size': 40, 'color': COLORS['text']}},
        domain={'x': [0, 1], 'y': [0, 1]},
        title={
            'text': "<b>Return on Investment</b><br><span style='font-size:0.8em;color:gray'>Based on Annual Net Income</span>",
            'font': {'size': 8, 'color': COLORS['text'], 'family': 'Inter'},
            'align': 'center'
        },
        gauge={
            'axis': {'range': [None, 20], 'tickwidth': 1, 'tickcolor': COLORS['text']},
            'bar': {'color': COLORS['primary']},
            'steps': [
                {'range': [0, 4], 'color': COLORS['danger']},
                {'range': [4, 8], 'color': COLORS['warning']},
                {'range': [8, 12], 'color': COLORS['secondary']},
                {'range': [12, 20], 'color': COLORS['success']}
            ],
            'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': roi
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='white',
        height=300,
        margin=dict(t=40, b=20, l=20, r=20)
    )
    
    return fig

def create_income_summary(df, properties):
    """Create simple monthly income trend visualization"""
    filtered_df = df[df['Location'].isin(properties)]
    monthly_data = filtered_df.groupby('YearMonth').agg({
        'Total_Income': 'sum',
        'Total_Expenses': 'sum',
        'Net_Income': 'sum'
    }).reset_index()
    
    fig = go.Figure()
    
    # Add income and expense lines
    fig.add_trace(go.Scatter(
        x=monthly_data['YearMonth'],
        y=monthly_data['Total_Income'],
        name='Income',
        line=dict(color=COLORS['secondary'], width=2),
        hovertemplate='Month: %{x}<br>Income: $%{y:,.2f}<extra></extra>'
    ))
    
    fig.add_trace(go.Scatter(
        x=monthly_data['YearMonth'],
        y=monthly_data['Total_Expenses'],
        name='Expenses',
        line=dict(color=COLORS['warning'], width=2),
        hovertemplate='Month: %{x}<br>Expenses: $%{y:,.2f}<extra></extra>'
    ))
    
    # Calculate average monthly income and expenses
    avg_income = monthly_data['Total_Income'].mean()
    avg_expenses = monthly_data['Total_Expenses'].mean()
    
    title_text = (
        "Monthly Income and Expenses<br>"
        f"<span style='font-size: 12px'>"
        f"Average Monthly Income: ${avg_income:,.0f} | "
        f"Average Monthly Expenses: ${avg_expenses:,.0f}"
        "</span>"
    )
    
    fig.update_layout(
        title=dict(
            text=title_text,
            x=0.5,
            xanchor='center'
        ),
        paper_bgcolor='white',
        plot_bgcolor='rgba(0,0,0,0)',
        xaxis_title='Month',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        height=350,
        margin=dict(t=80, b=40, l=40, r=40)
    )
    
    return fig

def create_expense_breakdown(df, properties):
    """Create expense breakdown visualization"""
    filtered_df = df[df['Location'].isin(properties)]
    
    # Calculate monthly metrics
    expense_categories = {
        'Property_Management_Fees': 'Management',
        'Utilities': 'Utilities',
        'Strata_Fees': 'Strata',
        'Routine_Maintenance': 'Maintenance',
        'Council_Rates': 'Council Rates',
        'Other_Miscellaneous_Costs': 'Other'
    }
    
    expenses = filtered_df[expense_categories.keys()].mean()
    
    fig = go.Figure(data=[go.Pie(
        labels=list(expense_categories.values()),
        values=expenses.values,
        hole=0.4,
        marker=dict(colors=COLORS['chart_colors'])
    )])
    
    fig.update_layout(
        title="Monthly Expense Breakdown",
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        height=400,
        margin=dict(t=40, b=80, l=20, r=20)
    )
    
    return fig

def create_expense_metrics_table(df, properties):
    """Create expense metrics table"""
    filtered_df = df[df['Location'].isin(properties)]
    
    metrics = {
        'Total Operating Expenses': filtered_df['Operating_Expenses'].sum(),
        'Average Monthly Expenses': filtered_df['Operating_Expenses'].mean(),
        'Highest Monthly Expense': filtered_df['Operating_Expenses'].max(),
        'Lowest Monthly Expense': filtered_df['Operating_Expenses'].min(),
        'Expense to Income Ratio': (filtered_df['Operating_Expenses'].sum() / 
                                  filtered_df['Gross_Income'].sum() * 100),
        'Average Cost per Property': filtered_df.groupby('Location')['Operating_Expenses'].mean().mean(),
        'Monthly Expense Volatility': filtered_df['Operating_Expenses'].std(),
        'Maintenance Cost Ratio': (filtered_df['Routine_Maintenance'].sum() / 
                                 filtered_df['Operating_Expenses'].sum() * 100)
    }
    
    fig = go.Figure(data=[go.Table(
        header=dict(
            values=['Metric', 'Value'],
            fill_color=COLORS['primary'],
            align='left',
            font=dict(color='white', size=12),
            height=40
        ),
        cells=dict(
            values=[
                list(metrics.keys()),
                [
                    f"${metrics['Total Operating Expenses']:,.2f}",
                    f"${metrics['Average Monthly Expenses']:,.2f}",
                    f"${metrics['Highest Monthly Expense']:,.2f}",
                    f"${metrics['Lowest Monthly Expense']:,.2f}",
                    f"{metrics['Expense to Income Ratio']:.1f}%",
                    f"${metrics['Average Cost per Property']:,.2f}",
                    f"${metrics['Monthly Expense Volatility']:,.2f}",
                    f"{metrics['Maintenance Cost Ratio']:.1f}%"
                ]
            ],
            align='left',
            fill_color=[[COLORS['background']]],
            font=dict(color=COLORS['text'], size=12),
            height=35
        )
    )])
    
    fig.update_layout(
        margin=dict(t=0, b=0, l=0, r=0),
        height=350
    )
    
    return fig

def create_expense_trends(df, properties):
    """Create expense trends visualization"""
    filtered_df = df[df['Location'].isin(properties)]
    monthly_data = filtered_df.groupby('YearMonth')[['Operating_Expenses', 'Routine_Maintenance']].sum().reset_index()
    
    fig = go.Figure()
    
    # Add expense line
    fig.add_trace(go.Scatter(
        x=monthly_data['YearMonth'],
        y=monthly_data['Operating_Expenses'],
        name='Total Expenses',
        line=dict(color=COLORS['primary'], width=2)
    ))
    
    # Add maintenance line
    fig.add_trace(go.Scatter(
        x=monthly_data['YearMonth'],
        y=monthly_data['Routine_Maintenance'],
        name='Maintenance',
        line=dict(color=COLORS['secondary'], width=2)
    ))
    
    fig.update_layout(
        title="Monthly Expense Trends",
        xaxis_title="Month",
        yaxis_title="Amount ($)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400,
        margin=dict(t=60, b=40, l=60, r=40),
        yaxis_tickformat='$,.0f'
    )
    
    return fig

def create_financial_forecast(df, properties, forecast_months=12):
    """Create financial forecast visualization"""
    filtered_df = df[df['Location'].isin(properties)]
    
    # Calculate historical monthly income
    monthly_income = filtered_df.groupby('YearMonth')['Net_Income'].mean().reset_index()
    monthly_income['Growth'] = monthly_income['Net_Income'].pct_change()
    
    # Calculate forecast parameters
    avg_growth_rate = monthly_income['Growth'].mean()
    growth_std = monthly_income['Growth'].std()
    last_value = monthly_income['Net_Income'].iloc[-1]
    last_date = pd.to_datetime(monthly_income['YearMonth'].iloc[-1])
    
    # Generate forecast
    forecast_dates = pd.date_range(start=last_date, periods=forecast_months+1, freq='M')[1:]
    forecast_values = []
    upper_bound = []
    lower_bound = []
    current_value = last_value
    
    for _ in range(forecast_months):
        current_value *= (1 + avg_growth_rate)
        forecast_values.append(current_value)
        upper_bound.append(current_value * (1 + growth_std))
        lower_bound.append(current_value * (1 - growth_std))
    
    fig = go.Figure()
    
    # Add historical data
    fig.add_trace(go.Scatter(
        x=monthly_income['YearMonth'],
        y=monthly_income['Net_Income'],
        name='Historical',
        line=dict(color=COLORS['primary'], width=2)
    ))
    
    # Add forecast
    fig.add_trace(go.Scatter(
        x=forecast_dates.strftime('%Y-%m'),
        y=forecast_values,
        name='Forecast',
        line=dict(color=COLORS['accent'], dash='dash')
    ))
    
    # Add confidence interval
    fig.add_trace(go.Scatter(
        x=forecast_dates.strftime('%Y-%m'),
        y=upper_bound,
        fill=None,
        mode='lines',
        line_color='rgba(0,0,0,0)',
        showlegend=False
    ))
    
    fig.add_trace(go.Scatter(
        x=forecast_dates.strftime('%Y-%m'),
        y=lower_bound,
        fill='tonexty',
        mode='lines',
        line_color='rgba(0,0,0,0)',
        name='Confidence Interval',
        fillcolor='rgba(33, 150, 243, 0.2)'
    ))
    
    fig.update_layout(
        title={
            'text': f"Income Forecast - Next {forecast_months} Months",
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top'
        },
        xaxis_title="Month",
        yaxis_title="Income ($)",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=500,
        margin=dict(t=80, b=40, l=60, r=40),
        yaxis_tickformat='$,.0f'
    )
    
    return fig

# Callbacks
@app.callback(
    Output('tab-content', 'children'),
    [Input('tabs', 'value'),
     Input('property-dropdown', 'value'),
     Input('time-format', 'value'),
     Input('update-button', 'n_clicks')],
    [State('purchase-price', 'value'),
     State('down-payment', 'value'),
     State('interest-rate', 'value')]
)
def render_tab_content(tab, properties, time_format, n_clicks, purchase_price, down_payment, interest_rate):
    if not properties:
        return html.Div([
            html.H3(
                "Please select at least one property",
                style={
                    'textAlign': 'center',
                    'color': COLORS['text'],
                    'marginTop': '50px'
                }
            )
        ])

    if tab == 'tab-1':  # Overview
        return html.Div([
            # Top row
            html.Div([
                html.Div([
                    dcc.Graph(
                        figure=create_roi_gauge(df, properties, purchase_price, down_payment),
                        config={'displayModeBar': False}
                    )
                ], className='chart-container', style={'width': '48%'}),
                
                html.Div([
                    html.Div([
                        html.Div("Monthly Net Income", className='metric-label'),
                        html.Div(
                            f"${df[df['Location'].isin(properties)]['Net_Income'].mean():,.2f}",
                            className='metric-value'
                        )
                    ], className='metric-card'),
                    html.Div([
                        html.Div("Occupancy Rate", className='metric-label'),
                        html.Div(
                            f"{(1 - df[df['Location'].isin(properties)]['Vacancy_Status'].mean()) * 100:.1f}%",
                            className='metric-value'
                        )
                    ], className='metric-card', style={'marginTop': '20px'})
                ], className='chart-container', style={'width': '48%'})
            ], style={
                'display': 'flex',
                'justifyContent': 'space-between',
                'marginBottom': '20px'
            }),
            
            # Bottom row - Income Summary Graph
            html.Div([
                dcc.Graph(
                    figure=create_income_summary(df, properties),
                    config={'displayModeBar': True}
                )
            ], className='chart-container')
        ])

    elif tab == 'tab-2':  # Expense Analysis
        return html.Div([
            html.Div([
                dcc.Graph(
                    figure=create_expense_metrics_table(df, properties),
                    config={'displayModeBar': False}
                )
            ], className='chart-container'),
            
            html.Div([
                dcc.Graph(
                    figure=create_expense_breakdown(df, properties),
                    config={'displayModeBar': False}
                )
            ], className='chart-container'),
            
            html.Div([
                dcc.Graph(
                    figure=create_expense_trends(df, properties),
                    config={'displayModeBar': True}
                )
            ], className='chart-container')
        ])

    elif tab == 'tab-4':  # Financial Forecasting
        return html.Div([
            html.Div([
                dcc.Graph(
                    figure=create_financial_forecast(df, properties),
                    config={'displayModeBar': True}
                )
            ], className='chart-container')
        ])

@app.callback(
    Output('property-map', 'figure'),
    [Input('property-dropdown', 'value')]
)
def update_map(selected_properties):
    if not selected_properties:
        return px.scatter_mapbox().update_layout(
            mapbox_style="open-street-map",
            margin=dict(r=0, t=0, l=0, b=0),
            height=200
        )
    
    filtered_data = property_data[property_data['Location'].isin(selected_properties)]
    
    lat_center = filtered_data['Latitude'].mean()
    lon_center = filtered_data['Longitude'].mean()
    
    fig = px.scatter_mapbox(
        filtered_data,
        lat='Latitude',
        lon='Longitude',
        hover_name='Property',
        height=200,
        zoom=12
    )
    
    fig.update_traces(
        marker=dict(size=20, color=COLORS['primary'])
    )
    
    fig.update_layout(
        mapbox=dict(
            style="open-street-map",
            center=dict(lat=lat_center, lon=lon_center)
        ),
        margin=dict(r=0, t=0, l=0, b=0),
        showlegend=False
    )
    
    return fig

@app.callback(
    [Output('purchase-price', 'style'),
     Output('down-payment', 'style'),
     Output('interest-rate', 'style')],
    [Input('purchase-price', 'value'),
     Input('down-payment', 'value'),
     Input('interest-rate', 'value')]
)
def validate_inputs(purchase_price, down_payment, interest_rate):
    base_style = {
        'width': 'calc(100% - 25px)',
        'height': '38px',
        'padding': '8px 12px',
        'paddingLeft': '25px',
        'borderRadius': '6px',
        'fontSize': '14px'
    }
    
    error_style = {**base_style, 'border': f'1px solid {COLORS["danger"]}'}
    valid_style = {**base_style, 'border': f'1px solid {COLORS["border"]}'}
    
    styles = [valid_style.copy() for _ in range(3)]
    
    if not purchase_price or purchase_price <= 0:
        styles[0] = error_style
    
    if not down_payment or down_payment <= 0 or (purchase_price and down_payment >= purchase_price):
        styles[1] = error_style
    
    if not interest_rate or interest_rate < 0 or interest_rate > 20:
        styles[2] = error_style
    
    return styles

if __name__ == '__main__':
    app.run_server(debug=True, port=8050)
