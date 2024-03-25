import pandas as pd
import plotly.express as px
import streamlit as st

# Function to read CSV file and process data
def process_data(file_path, top_n):
    query_df = pd.read_csv(file_path)

    word_freq_dfs = []
    for date in sorted(query_df['date'].drop_duplicates()):
        temp_df = query_df[query_df['date'].eq(date)]
        query_metric = pd.pivot_table(temp_df, index='query', values='clicks', aggfunc='sum').reset_index()
        word_freq_df = query_metric.nlargest(top_n, 'clicks')
        word_freq_df.insert(0, 'date', temp_df['date'].iloc[0])
        word_freq_dfs.append(word_freq_df)

    return pd.concat(word_freq_dfs)

# Main Streamlit app
def main():
    st.title('Google Search Console (GSC) Queries Race Chart')

    # Upload CSV file
    uploaded_file = st.file_uploader('Upload CSV file', type=['csv'])
    if uploaded_file is not None:
        # Read and process the uploaded CSV file
        df = process_data(uploaded_file, 15)  # Assuming top_n = 15

        # Create a racing bar chart using Plotly
        fig = px.bar(df, x='clicks', y='query', animation_frame='date', orientation='h',
                     title='Top Queries Daily Trends - Clicks')

        # Adjust layout if needed
        fig.update_layout(height=800)

        # Modify date format for animation frames
        date_format = '%d %B %Y'  # Example: 16 March 2023
        fig.update_xaxes(dtick=1, tickformat=date_format)

        # Display the racing chart
        st.plotly_chart(fig, use_container_width=True)

# Run the app
if __name__ == '__main__':
    main()
