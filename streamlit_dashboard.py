import pandas as pd  
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import os
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Hotel Booking Dashboard",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main > div {
        padding-top: 2rem;
    }
    h1 {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# Data loading functions
@st.cache_data
def load_data(filepath):
    """Load hotel booking data from CSV file."""
    try:
        df = pd.read_csv(filepath)
        return df
    except FileNotFoundError:
        st.error(f"❌ File '{filepath}' not found!")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error reading file: {e}")
        st.stop()

@st.cache_data
def load_countries_data(filepath):
    """Load countries location data from CSV file."""
    try:
        countries = pd.read_csv(filepath)
        countries = countries.rename(columns={"Latitude": "lat", "Longitude": "lon"})
        return countries
    except FileNotFoundError:
        st.error(f"❌ Countries file '{filepath}' not found!")
        st.stop()
    except Exception as e:
        st.error(f"❌ Error reading countries file: {e}")
        st.stop()

def prepare_date_columns(df):
    """Prepare date-related columns for analysis."""
    df_copy = df.copy()
    if 'arrival_date' in df_copy.columns:
        df_copy["arrival_date"] = pd.to_datetime(df_copy["arrival_date"], errors='coerce')
        df_copy["day_of_year"] = df_copy["arrival_date"].dt.day_of_year
    return df_copy

# Visualization functions
def create_choropleth_map(countries_data):
    """Create choropleth map showing country distribution."""
    fig = px.choropleth(
        countries_data,
        locations="Country_Code",
        color="Count",
        hover_name="Country_Code",
        color_continuous_scale=[
            (0.0, "lightblue"),
            (0.5, "blue"),
            (1.0, "darkblue")
        ],
        projection="natural earth",
        title="🌍 Country Distribution by Booking Count",
    )
    
    fig.update_layout(
        template="plotly_dark",
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
        plot_bgcolor="rgba(0, 0, 0, 0)",
        paper_bgcolor="rgba(0, 0, 0, 0)",
        margin=dict(l=0, r=0, t=40, b=0),
        height=500
    )
    
    return fig

def create_sunburst_chart(df):
    """Create sunburst chart for revenue analysis."""
    fig = px.sunburst(
        data_frame=df,
        path=['hotel', 'customer_type', 'meal'],
        values='total_nights',
        title="📊 Total Nights by Hotel Type, Customer Type & Meal"
    )
    fig.update_layout(margin=dict(l=0, r=0, t=40, b=0))
    return fig

def create_lead_time_bar(df):
    """Create bar chart for lead time by market segment."""
    fig = px.bar(
        data_frame=df,
        x='market_segment',
        y='lead_time',
        color='is_canceled',
        title="📅 Lead Time by Market Segment",
        labels={'lead_time': 'Lead Time (days)', 'market_segment': 'Market Segment'}
    )
    return fig

def create_customer_type_pie(df):
    """Create pie chart for customer type distribution."""
    fig = go.Figure(data=[go.Pie(
        labels=df['customer_type'].unique(),
        values=df['customer_type'].value_counts(),
        hole=.3
    )])
    fig.update_layout(title="👥 Customer Type Distribution")
    return fig

def create_adr_by_month(df):
    """Create grouped bar chart for ADR by month."""
    fig = px.bar(
        data_frame=df,
        y='adr',
        x='arrival_date_month',
        color='hotel',
        barmode='group',
        title="💰 Average Daily Rate by Month",
        labels={'arrival_date_month': 'Month', 'adr': 'Average Daily Rate ($)'}
    )
    return fig

def create_season_distribution(df):
    """Create bar chart for seasonal distribution."""
    fig = px.bar(
        data_frame=df,
        x='season',
        color='hotel',
        title="🌤️ Bookings by Season",
        labels={'season': 'Season', 'count': 'Number of Bookings'}
    )
    return fig

def create_lead_time_histogram(df):
    """Create histogram for lead time distribution."""
    fig = px.histogram(
        data_frame=df,
        x='lead_time',
        color='is_canceled',
        title="📊 Lead Time Distribution",
        labels={'lead_time': 'Lead Time (days)'},
        nbins=50
    )
    return fig

def create_daily_arrivals_scatter(df):
    """Create scatter plot for daily arrivals throughout the year."""
    daily_counts = (
        df.groupby(["day_of_year", "hotel"])
          .size()
          .reset_index(name="count")
    )
    
    fig = px.scatter(
        daily_counts,
        x="day_of_year",
        y="count",
        color="hotel",
        labels={
            "day_of_year": "Day of Year",
            "count": "Number of Reservations",
            "hotel": "Hotel Type"
        },
        title="📅 Daily Hotel Arrivals Throughout the Year"
    )
    return fig

def create_polar_revenue_chart(df):
    """Create polar chart for revenue by customer type."""
    df_polar = (
        df.groupby(['hotel', 'customer_type'], as_index=False)
          .agg(total_revenue=('total_revenue', 'sum'))
    )
    
    fig = px.line_polar(
        data_frame=df_polar,
        r='total_revenue',
        theta='customer_type',
        color='hotel',
        line_close=True,
        title='💵 Total Revenue by Customer Type',
        template="plotly_dark"
    )
    return fig

def create_adr_leadtime_scatter(df):
    """Create scatter plot for ADR vs Lead Time."""
    fig = px.scatter(
        data_frame=df,
        x='adr',
        y='lead_time',
        size='total_nights',
        color='hotel',
        title='📈 Lead Time vs Average Daily Rate',
        labels={'adr': 'Average Daily Rate ($)', 'lead_time': 'Lead Time (days)'}
    )
    return fig

# Main application
def main():
    st.title('🏨 Hotel Booking Dashboard')
    
    # File paths
    data_file = 'hotel_booking_cleaned.csv'
    countries_file = 'countries_loc.csv'
    
    # Load data
    df_original = load_data(data_file)
    countries = load_countries_data(countries_file)
    
    # Prepare date columns
    df_original = prepare_date_columns(df_original)
    
    # Sidebar filters
    st.sidebar.header("🔍 Filters")
    
    # Initialize filtered dataframe
    df_filtered = df_original.copy()
    
    # Hotel type filter
    if 'hotel' in df_filtered.columns:
        hotel_types = st.sidebar.multiselect(
            'Hotel Type',
            options=df_filtered['hotel'].unique(),
            default=df_filtered['hotel'].unique()
        )
        df_filtered = df_filtered[df_filtered['hotel'].isin(hotel_types)]
    
    # Customer type filter
    if 'customer_type' in df_filtered.columns:
        customer_types = st.sidebar.multiselect(
            'Customer Type',
            options=df_filtered['customer_type'].unique(),
            default=df_filtered['customer_type'].unique()
        )
        df_filtered = df_filtered[df_filtered['customer_type'].isin(customer_types)]
    
    # Cancellation filter
    if 'is_canceled' in df_filtered.columns:
        cancellation_filter = st.sidebar.radio(
            'Booking Status',
            options=['All', 'Not Canceled', 'Canceled'],
            index=0
        )
        if cancellation_filter == 'Not Canceled':
            df_filtered = df_filtered[df_filtered['is_canceled'] == 0]
        elif cancellation_filter == 'Canceled':
            df_filtered = df_filtered[df_filtered['is_canceled'] == 1]
    
    # Date range filter
    if 'arrival_date' in df_filtered.columns:
        st.sidebar.subheader("📅 Date Range")
        min_date = df_filtered['arrival_date'].min()
        max_date = df_filtered['arrival_date'].max()
        
        if pd.notna(min_date) and pd.notna(max_date):
            date_range = st.sidebar.date_input(
                "Select Date Range",
                value=(min_date, max_date),
                min_value=min_date,
                max_value=max_date
            )
            
            if len(date_range) == 2:
                start_date, end_date = date_range
                df_filtered = df_filtered[
                    (df_filtered['arrival_date'] >= pd.to_datetime(start_date)) &
                    (df_filtered['arrival_date'] <= pd.to_datetime(end_date))
                ]
    
    # Advanced filters
    with st.sidebar.expander("⚙️ Advanced Filters"):
        if 'adr' in df_filtered.columns:
            adr_range = st.slider(
                'Average Daily Rate ($)',
                float(df_original['adr'].min()),
                float(df_original['adr'].max()),
                (float(df_original['adr'].min()), float(df_original['adr'].max()))
            )
            df_filtered = df_filtered[
                (df_filtered['adr'] >= adr_range[0]) &
                (df_filtered['adr'] <= adr_range[1])
            ]
        
        if 'lead_time' in df_filtered.columns:
            max_lead_time = st.number_input(
                'Max Lead Time (days)',
                min_value=0,
                max_value=int(df_original['lead_time'].max()),
                value=int(df_original['lead_time'].max())
            )
            df_filtered = df_filtered[df_filtered['lead_time'] <= max_lead_time]
    
    # Show filter info
    st.sidebar.info(f"📊 Showing {len(df_filtered):,} of {len(df_original):,} bookings")
    
    # Download filtered data
    if st.sidebar.button("⬇️ Download Filtered Data"):
        csv = df_filtered.to_csv(index=False)
        st.sidebar.download_button(
            label="Download CSV",
            data=csv,
            file_name=f"filtered_bookings_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
            mime="text/csv"
        )
    
    # Main dashboard content
    # Country map
    with st.container(border=True):
        st.plotly_chart(create_choropleth_map(countries), use_container_width=True)
    
    # Key metrics
    cols = st.columns(4)
    with cols[0]:
        with st.container(border=True, height=120):
            st.metric(
                label="🌍 Countries",
                value=len(df_filtered['country'].unique()) if 'country' in df_filtered.columns else 0
            )
    with cols[1]:
        with st.container(border=True, height=120):
            st.metric(
                label="👥 Total Bookings",
                value=f"{len(df_filtered):,}"
            )
    with cols[2]:
        with st.container(border=True, height=120):
            resort_count = df_filtered['hotel'].value_counts().get('Resort Hotel', 0) if 'hotel' in df_filtered.columns else 0
            st.metric(
                label="🏖️ Resort Hotels",
                value=f"{resort_count:,}"
            )
    with cols[3]:
        with st.container(border=True, height=120):
            city_count = df_filtered['hotel'].value_counts().get('City Hotel', 0) if 'hotel' in df_filtered.columns else 0
            st.metric(
                label="🏙️ City Hotels",
                value=f"{city_count:,}"
            )
    
    # Row 1: Three charts
    cols2 = st.columns(3)
    with cols2[0]:
        with st.container(border=True):
            st.plotly_chart(create_polar_revenue_chart(df_filtered), use_container_width=True)
    with cols2[1]:
        with st.container(border=True):
            st.plotly_chart(create_adr_by_month(df_filtered), use_container_width=True)
    with cols2[2]:
        with st.container(border=True):
            st.plotly_chart(create_season_distribution(df_filtered), use_container_width=True)
    
    # Row 2: Lead time histogram
    with st.container(border=True):
        st.plotly_chart(create_lead_time_histogram(df_filtered), use_container_width=True)
    
    # Row 3: Two charts
    cols5 = st.columns(2)
    with cols5[0]:
        with st.container(border=True):
            st.plotly_chart(create_sunburst_chart(df_filtered), use_container_width=True)
    with cols5[1]:
        with st.container(border=True):
            st.plotly_chart(create_adr_leadtime_scatter(df_filtered), use_container_width=True)
    
    # Row 4: Daily arrivals
    with st.container(border=True):
        st.plotly_chart(create_daily_arrivals_scatter(df_filtered), use_container_width=True)
    
    # Data explorer section
    with st.expander("📋 View Data Table"):
        st.subheader('Filtered Booking Data')
        st.dataframe(df_filtered, use_container_width=True, height=400)
        
        # Country breakdown
        st.subheader('📍 Top 10 Countries by Bookings')
        if 'country' in df_filtered.columns:
            country_counts = df_filtered['country'].value_counts().head(10)
            st.bar_chart(country_counts)

if __name__ == "__main__":
    main()
