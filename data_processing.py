import pandas as pd
import numpy as np

# Vehicle configuration with prices, categories, and dealer margins
vehicle_mapping = {
    'H F 100': {
        'name': 'HF100',
        'price': 70000,
        'category': 'Commuter Motorcycle',
        'margin': 0.08  # 8% dealer margin
    },
    'SPLENDOR +': {
        'name': 'Splendor+',
        'price': 90000,
        'category': 'Commuter Motorcycle',
        'margin': 0.08
    },
    'SPLENDOR + XTEC2.0': {
        'name': 'Splendor+ XTEC',
        'price': 98000,
        'category': 'Commuter Motorcycle',
        'margin': 0.08
    },
    'SUPER SPLENDOR XTEC': {
        'name': 'Super Splendor XTEC',
        'price': 105000,
        'category': 'Commuter Motorcycle',
        'margin': 0.08
    },
    'PASSION +': {
        'name': 'Passion+',
        'price': 95000,
        'category': 'Commuter Motorcycle',
        'margin': 0.08
    },
    'XTREME 125': {
        'name': 'Xtreme 125R',
        'price': 110000,
        'category': 'Sports/Premium Motorcycle',
        'margin': 0.10  # 10% dealer margin
    },
    'X PULSE 200': {
        'name': 'X Pulse 200',
        'price': 180000,
        'category': 'Sports/Premium Motorcycle',
        'margin': 0.10
    },
    'PLEASUR +': {
        'name': 'Pleasure+',
        'price': 85000,
        'category': 'Scooter',
        'margin': 0.09  # 9% dealer margin
    },
    'PLEASURE  XTEC': {
        'name': 'Pleasure XTEC',
        'price': 92000,
        'category': 'Scooter',
        'margin': 0.09
    },
    'XOOM': {
        'name': 'Xoom',
        'price': 90000,
        'category': 'Scooter',
        'margin': 0.09
    },
    'DESTINI 125': {
        'name': 'Destini 125',
        'price': 105000,
        'category': 'Scooter',
        'margin': 0.09
    },
    'VIDA VX2 PLUS': {
        'name': 'Vida VX2 Plus',
        'price': 120000,
        'category': 'EV Scooter',
        'margin': 0.12  # 12% dealer margin
    }
}

# Chronological month mapping (April 2025 to April 2026)
month_date_map = {
    'APRIL': ('April 2025', '2025-04-01', 'Summer'),
    'MAY': ('May 2025', '2025-05-01', 'Summer'),
    'JUNE': ('June 2025', '2025-06-01', 'Summer'),
    'JULY': ('July 2025', '2025-07-01', 'Monsoon'),
    'AUGUST': ('August 2025', '2025-08-01', 'Monsoon'),
    'SEPTEMBER': ('September 2025', '2025-09-01', 'Monsoon'),
    'OCTOBER': ('October 2025', '2025-10-01', 'Festive/Autumn'),
    'NAVEMBER': ('November 2025', '2025-11-01', 'Festive/Autumn'),
    'DECEMBER': ('December 2025', '2025-12-01', 'Winter'),
    'JANUARY': ('January 2026', '2026-01-01', 'Winter'),
    'FEBRUARY': ('February 2026', '2026-02-01', 'Winter'),
    'MARCH': ('March 2026', '2026-03-01', 'Spring'),
    'APRIL.1': ('April 2026', '2026-04-01', 'Summer')
}

def get_demand_level(units):
    if units <= 2:
        return 'Low'
    elif units <= 7:
        return 'Medium'
    else:
        return 'High'

def main():
    print("Loading Excel dataset...")
    # Load sheet, row index 2 has column names (SL NO, VEHICLE, APRIL, etc.)
    df = pd.read_excel('JAYA MOTORS SALE.xlsx', header=2)
    
    # Strip whitespace from columns
    df.columns = df.columns.str.strip()
    
    # Remove 'TOTAL' summary row and null rows
    df = df[df['VEHICLE'].notna()]
    df = df[df['VEHICLE'].str.strip() != 'TOTAL']
    
    # Define columns to melt
    months_cols = ['APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER', 'NAVEMBER', 'DECEMBER', 'JANUARY', 'FEBRUARY', 'MARCH', 'APRIL.1']
    
    print("Melting dataset into long format...")
    # Melt dataset
    df_melted = df.melt(id_vars=['VEHICLE'], value_vars=months_cols, var_name='Month_Raw', value_name='Units_Sold')
    
    # Fill missing sales with 0 units
    df_melted['Units_Sold'] = df_melted['Units_Sold'].fillna(0).astype(int)
    
    # Map Vehicle properties
    print("Mapping vehicle attributes and prices...")
    df_melted['Vehicle'] = df_melted['VEHICLE'].apply(lambda x: vehicle_mapping.get(x.strip(), {}).get('name', x.strip()))
    df_melted['Price'] = df_melted['VEHICLE'].apply(lambda x: vehicle_mapping.get(x.strip(), {}).get('price', 0))
    df_melted['Category'] = df_melted['VEHICLE'].apply(lambda x: vehicle_mapping.get(x.strip(), {}).get('category', 'Unknown'))
    df_melted['Margin'] = df_melted['VEHICLE'].apply(lambda x: vehicle_mapping.get(x.strip(), {}).get('margin', 0.0))
    
    # Map Month properties
    print("Mapping chronological date fields and seasons...")
    df_melted['Month'] = df_melted['Month_Raw'].map(lambda x: month_date_map[x][0])
    df_melted['Date'] = df_melted['Month_Raw'].map(lambda x: month_date_map[x][1])
    df_melted['Season'] = df_melted['Month_Raw'].map(lambda x: month_date_map[x][2])
    
    # Calculations
    print("Calculating revenue and profit...")
    df_melted['Revenue'] = df_melted['Units_Sold'] * df_melted['Price']
    df_melted['Profit'] = (df_melted['Revenue'] * df_melted['Margin']).astype(int)
    df_melted['Demand'] = df_melted['Units_Sold'].apply(get_demand_level)
    
    # Select and reorder columns for output
    output_cols = ['Date', 'Month', 'Vehicle', 'Units_Sold', 'Price', 'Revenue', 'Profit', 'Category', 'Demand', 'Season']
    final_df = df_melted[output_cols].sort_values(by=['Date', 'Vehicle']).reset_index(drop=True)
    
    # Export to CSV
    output_filename = 'processed_sales_data.csv'
    final_df.to_csv(output_filename, index=False)
    print(f"Dataset successfully processed and exported to '{output_filename}'!")
    
    # Print basic summary metrics
    print("\n--- Summary Insights ---")
    total_sales = final_df['Units_Sold'].sum()
    total_revenue = final_df['Revenue'].sum()
    total_profit = final_df['Profit'].sum()
    print(f"Total Sales: {total_sales} units")
    print(f"Total Revenue: Rs. {total_revenue:,}")
    print(f"Total Profit: Rs. {total_profit:,}")
    
    # Vehicle sales summary
    vehicle_summary = final_df.groupby('Vehicle').agg(
        Total_Units=('Units_Sold', 'sum'),
        Total_Rev=('Revenue', 'sum')
    ).sort_values(by='Total_Units', ascending=False)
    
    print(f"Best Selling Vehicle: {vehicle_summary.index[0]} ({vehicle_summary.iloc[0]['Total_Units']} units)")
    print(f"Lowest Selling Vehicle: {vehicle_summary.index[-1]} ({vehicle_summary.iloc[-1]['Total_Units']} units)")
    print(f"Highest Revenue Vehicle: {vehicle_summary.sort_values(by='Total_Rev', ascending=False).index[0]} (Rs. {vehicle_summary.sort_values(by='Total_Rev', ascending=False).iloc[0]['Total_Rev']:,})")
    
    # Monthly sales summary
    monthly_summary = final_df.groupby(['Date', 'Month'])['Units_Sold'].sum().reset_index().sort_values(by='Units_Sold', ascending=False)
    print(f"Best Sales Month: {monthly_summary.iloc[0]['Month']} ({monthly_summary.iloc[0]['Units_Sold']} units)")

if __name__ == '__main__':
    main()
