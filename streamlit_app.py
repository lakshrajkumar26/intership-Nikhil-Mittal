import streamlit as st
import pandas as pd
import numpy as np
import yfinance as yf
import requests
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from dateutil import parser
import json
import warnings
warnings.filterwarnings('ignore')

# Import the PortfolioAnalyzer class
from portfolio_analyzer import PortfolioAnalyzer

def create_demo_data():
    """Create demo CSV files matching the exact format of user's data"""
    import pandas as pd
    import numpy as np
    from datetime import datetime, timedelta
    
    # Create demo data for 2023 (matching user's format exactly)
    demo_data_2023 = [
        {
            'Trades': 'Trades',
            'Header': 'Header',
            'DataDiscriminator': 'Data',
            'Asset Category': 'Stocks',
            'Currency': 'USD',
            'Symbol': 'AMZN',
            'Date/Time': '2023-07-21, 13:57:21',
            'Quantity': 50,
            'T. Price': 130.478,
            'C. Price': 130,
            'Proceeds': -6523.9,
            'Comm/Fee': -1.078,
            'Basis': 6524.978,
            'Realized P/L': 0,
            'MTM P/L': -23.9,
            'Code': 'O'
        },
        {
            'Trades': 'Trades',
            'Header': 'Header',
            'DataDiscriminator': 'Data',
            'Asset Category': 'Stocks',
            'Currency': 'USD',
            'Symbol': 'GOOG',
            'Date/Time': '2023-07-31, 13:11:02',
            'Quantity': 50,
            'T. Price': 132.66,
            'C. Price': 133.11,
            'Proceeds': -6633,
            'Comm/Fee': -1.078,
            'Basis': 6634.078,
            'Realized P/L': 0,
            'MTM P/L': 22.5,
            'Code': 'O'
        },
        {
            'Trades': 'Trades',
            'Header': 'Header',
            'DataDiscriminator': 'Data',
            'Asset Category': 'Stocks',
            'Currency': 'USD',
            'Symbol': 'MSFT',
            'Date/Time': '2023-07-20, 12:54:31',
            'Quantity': 30,
            'T. Price': 348.24,
            'C. Price': 346.87,
            'Proceeds': -10447.2,
            'Comm/Fee': -1.0788,
            'Basis': 10448.2788,
            'Realized P/L': 0,
            'MTM P/L': -41.1,
            'Code': 'O'
        }
    ]
    
    df_2023 = pd.DataFrame(demo_data_2023)
    df_2023.to_csv('Stock_trading_2023.csv', index=False)
    
    # Create demo data for 2024 (matching user's format)
    demo_data_2024 = [
        {
            'Trades': 'Trades',
            'Header': 'Header',
            'DataDiscriminator': 'Data',
            'Asset Category': 'Stocks',
            'Currency': 'USD',
            'Symbol': 'NVDA',
            'Date/Time': '2024-01-15, 14:30:00',
            'Quantity': 40,
            'T. Price': 380,
            'C. Price': 374.75,
            'Proceeds': -15200,
            'Comm/Fee': -1.0784,
            'Basis': 15201.0784,
            'Realized P/L': 0,
            'MTM P/L': -210,
            'Code': 'O'
        },
        {
            'Trades': 'Trades',
            'Header': 'Header',
            'DataDiscriminator': 'Data',
            'Asset Category': 'Stocks',
            'Currency': 'USD',
            'Symbol': 'AAPL',
            'Date/Time': '2024-02-20, 13:45:00',
            'Quantity': 25,
            'T. Price': 150.25,
            'C. Price': 151.10,
            'Proceeds': -3756.25,
            'Comm/Fee': -1.078,
            'Basis': 3757.328,
            'Realized P/L': 0,
            'MTM P/L': 21.25,
            'Code': 'O'
        }
    ]
    
    df_2024 = pd.DataFrame(demo_data_2024)
    df_2024.to_csv('Stock_trading_2024.csv', index=False)
    
    # Create demo data for 2025 (matching user's format)
    demo_data_2025 = [
        {
            'Trades': 'Trades',
            'Header': 'Header',
            'DataDiscriminator': 'Data',
            'Asset Category': 'Stocks',
            'Currency': 'USD',
            'Symbol': 'TSLA',
            'Date/Time': '2025-01-10, 10:30:00',
            'Quantity': 30,
            'T. Price': 216.3,
            'C. Price': 212.08,
            'Proceeds': -6489,
            'Comm/Fee': -1.0788,
            'Basis': 6490.0788,
            'Realized P/L': 0,
            'MTM P/L': -126.6,
            'Code': 'O'
        }
    ]
    
    df_2025 = pd.DataFrame(demo_data_2025)
    df_2025.to_csv('Stock_trading_2025.csv', index=False)
    
    print("Demo data created successfully!")

# Custom CSS for modern UI
st.set_page_config(
    page_title="Portfolio Analyzer Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    .stButton > button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 1.5rem;
        font-weight: bold;
        box-shadow: 0 4px 15px rgba(0,0,0,0.2);
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(0,0,0,0.3);
    }
    
    .dataframe {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
    }
    
    .news-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
        color: white;
        box-shadow: 0 8px 32px rgba(0,0,0,0.1);
    }
    
    .news-title {
        font-size: 1.2rem;
        font-weight: bold;
        margin-bottom: 0.5rem;
        color: #ffffff;
    }
    
    .news-summary {
        font-size: 0.9rem;
        margin-bottom: 1rem;
        color: #f0f0f0;
    }
    
    .news-meta {
        font-size: 0.8rem;
        color: #d0d0d0;
        margin-bottom: 1rem;
    }
    
    .news-link {
        background: rgba(255,255,255,0.2);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        text-decoration: none;
        color: white;
        font-weight: bold;
        display: inline-block;
        transition: all 0.3s ease;
    }
    
    .news-link:hover {
        background: rgba(255,255,255,0.3);
        transform: translateY(-1px);
    }
    
    .welcome-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        color: white;
        text-align: center;
        margin: 2rem 0;
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
    }
    
    .feature-list {
        background: rgba(255,255,255,0.1);
        padding: 1.5rem;
        border-radius: 15px;
        margin: 1rem 0;
    }
    
    .feature-item {
        margin: 0.5rem 0;
        padding: 0.5rem;
        background: rgba(255,255,255,0.1);
        border-radius: 8px;
        border-left: 4px solid #ffffff;
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header
    st.markdown('<div class="main-header">🚀 Portfolio Analyzer Pro</div>', unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### ⚙️ Settings")
        
        # File upload section
        st.markdown("### 📁 Your Portfolio Data")
        
        # Check for existing CSV files first
        import os
        existing_files = []
        required_files = ['Stock_trading_2023.csv', 'Stock_trading_2024.csv', 'Stock_trading_2025.csv']
        
        for file in required_files:
            if os.path.exists(file):
                existing_files.append(file)
        
        if existing_files:
            st.success(f"✅ Found {len(existing_files)} data files:")
            for file in existing_files:
                st.write(f"📊 {file}")
            st.info("💡 Your actual portfolio data is ready for analysis!")
        else:
            st.warning("⚠️ No data files found. Please upload your CSV files:")
            st.write("Required files:")
            for file in required_files:
                st.write(f"- {file}")
        
        # File uploader for additional files
        uploaded_files = st.file_uploader(
            "Upload additional CSV files (optional)",
            type=['csv'],
            accept_multiple_files=True,
            help="Upload your Stock_trading_2023.csv, Stock_trading_2024.csv, and Stock_trading_2025.csv files"
        )
        
        if uploaded_files:
            st.success(f"✅ Uploaded {len(uploaded_files)} additional files")
            for file in uploaded_files:
                st.write(f"- {file.name}")
        
        st.markdown("---")
        
        # Analysis button
        if st.button("🔍 Run Portfolio Analysis", use_container_width=True):
            with st.spinner("Analyzing portfolio data..."):
                try:
                    # Initialize analyzer
                    analyzer = PortfolioAnalyzer()
                    
                    # Handle file analysis - prioritize user's actual files
                    import os
                    
                    # First, check for user's actual CSV files
                    user_files = ['Stock_trading_2023.csv', 'Stock_trading_2024.csv', 'Stock_trading_2025.csv']
                    available_files = []
                    
                    for file_path in user_files:
                        if os.path.exists(file_path):
                            available_files.append(file_path)
                    
                    # If uploaded files are provided, use them
                    if uploaded_files:
                        # Save uploaded files temporarily
                        for uploaded_file in uploaded_files:
                            file_path = uploaded_file.name
                            with open(file_path, 'wb') as f:
                                f.write(uploaded_file.getbuffer())
                            if file_path not in available_files:
                                available_files.append(file_path)
                        st.success(f"✅ Using files: {', '.join(available_files)}")
                    
                    # If no files available, show error
                    if not available_files:
                        st.error("❌ No portfolio data files found!")
                        st.write("**Required files:**")
                        for file in user_files:
                            st.write(f"- {file}")
                        st.write("**Please:**")
                        st.write("1. Upload your CSV files using the uploader above")
                        st.write("2. Or ensure your files are in the deployment")
                        st.write("3. Or use demo mode for testing")
                        
                        # Demo mode option
                        if st.button("🎯 Use Demo Mode", use_container_width=True):
                            st.info("🔄 Creating demo data...")
                            create_demo_data()
                            st.success("✅ Demo data created! Click 'Run Portfolio Analysis' again.")
                        return
                    
                    # Show which files will be used
                    if len(available_files) < len(user_files):
                        missing = [f for f in user_files if f not in available_files]
                        st.warning(f"⚠️ Some files missing: {', '.join(missing)}")
                        st.info(f"📊 Using available files: {', '.join(available_files)}")
                    else:
                        st.success(f"✅ Using all your portfolio data files!")
                    
                    # Run analysis with available files
                    success = analyzer.run_complete_analysis(available_files)
                    
                    if success:
                        st.session_state.analyzer = analyzer
                        st.session_state.analysis_complete = True
                        st.success("✅ Analysis completed successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Analysis failed. Please check your data files.")
                        
                except Exception as e:
                    st.error(f"❌ Error during analysis: {e}")
                    st.info("💡 Try uploading your CSV files or use demo mode.")
                    
                    # Show detailed error information
                    with st.expander("🔍 Debug Information"):
                        st.write("**Error Details:**")
                        st.code(str(e))
                        st.write("**Troubleshooting:**")
                        st.write("1. Make sure your CSV files have the correct format")
                        st.write("2. Check that files contain: Trades, DataDiscriminator, Date/Time, Symbol, Currency, Quantity, T. Price, C. Price, Proceeds")
                        st.write("3. Try the demo mode to test the application")
                        st.write("4. Ensure your files are not corrupted")
        
        st.markdown("---")
        st.markdown("### 📊 Features")
        st.markdown("""
        - 📈 Portfolio Analysis
        - 💰 XIRR Calculations
        - 📰 Real-time News
        - 🌍 Multi-currency Support
        - 📊 Interactive Charts
        """)
    
    # Main content
    if 'analysis_complete' in st.session_state and st.session_state.analysis_complete and hasattr(st.session_state, 'analyzer'):
        analyzer = st.session_state.analyzer
        
        # Portfolio Overview
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if hasattr(analyzer, 'portfolio_values') and not analyzer.portfolio_values.empty:
                latest_value = analyzer.portfolio_values['Value_USD'].iloc[-1]
                st.metric("Portfolio Value (USD)", f"${latest_value:,.2f}")
            else:
                st.metric("Portfolio Value (USD)", "Calculating...")
        
        with col2:
            if hasattr(analyzer, 'holdings') and not analyzer.holdings.empty:
                total_holdings = len(analyzer.holdings)
                st.metric("Total Holdings", f"{total_holdings} symbols")
            else:
                st.metric("Total Holdings", "Calculating...")
        
        with col3:
            if hasattr(analyzer, 'xirr_results') and analyzer.xirr_results:
                avg_xirr = np.mean(list(analyzer.xirr_results.values())) * 100
                st.metric("Average XIRR", f"{avg_xirr:.2f}%")
            else:
                st.metric("Average XIRR", "Calculating...")
        
        # Holdings Table
        st.markdown("### 📋 Current Holdings")
        if hasattr(analyzer, 'holdings') and not analyzer.holdings.empty:
            st.dataframe(analyzer.holdings, use_container_width=True)
        
        # Portfolio Performance Chart
        st.markdown("### 📈 Portfolio Performance")
        if hasattr(analyzer, 'portfolio_values') and not analyzer.portfolio_values.empty:
            fig = px.line(analyzer.portfolio_values, x='Date', y='Value_USD', 
                         title='Portfolio Value Over Time',
                         labels={'Value_USD': 'Portfolio Value (USD)', 'Date': 'Date'})
            fig.update_layout(height=400)
            st.plotly_chart(fig, use_container_width=True)
        
        # XIRR Results
        st.markdown("### 💰 XIRR Analysis")
        if hasattr(analyzer, 'xirr_results') and analyzer.xirr_results:
            xirr_df = pd.DataFrame(list(analyzer.xirr_results.items()), 
                                 columns=['Symbol', 'XIRR'])
            xirr_df['XIRR_Percentage'] = xirr_df['XIRR'] * 100
            st.dataframe(xirr_df, use_container_width=True)
        
        # News Section
        st.markdown("### 📰 Latest Market News & Analysis")
        
        col1, col2 = st.columns([3, 1])
        
        with col1:
            if hasattr(analyzer, 'holdings') and not analyzer.holdings.empty:
                symbols = analyzer.holdings['Symbol'].tolist()
                selected_symbol = st.selectbox("Select Symbol for News:", symbols)
            else:
                selected_symbol = st.selectbox("Select Symbol for News:", ["AAPL", "MSFT", "GOOGL"])
        
        with col2:
            if st.button("📰 Get News", use_container_width=True):
                with st.spinner("Fetching latest news..."):
                    try:
                        news_items = analyzer.get_latest_news(selected_symbol)
                        st.session_state.news_items = news_items
                        st.session_state.selected_symbol = selected_symbol
                        st.success(f"✅ Found {len(news_items)} news articles!")
                    except Exception as e:
                        st.error(f"❌ Error fetching news: {e}")
        
        # Display news
        if 'news_items' in st.session_state and 'selected_symbol' in st.session_state:
            if st.session_state.selected_symbol == selected_symbol:
                news_items = st.session_state.news_items
                
                for i, news in enumerate(news_items[:5]):
                    # Color code based on publisher/content
                    if any(word in news.get('publisher', '').lower() for word in ['bloomberg', 'reuters', 'cnbc']):
                        color_class = "news-card"
                    elif 'technical' in news.get('title', '').lower():
                        color_class = "news-card"
                    elif 'earnings' in news.get('title', '').lower():
                        color_class = "news-card"
                    else:
                        color_class = "news-card"
                    
                    st.markdown(f"""
                    <div class="{color_class}">
                        <div class="news-title">{news.get('title', 'No title')}</div>
                        <div class="news-summary">{news.get('summary', 'No summary available')}</div>
                        <div class="news-meta">
                            📅 {news.get('published', 'Unknown')} | 
                            📰 {news.get('publisher', 'Unknown')}
                        </div>
                        <a href="{news.get('link', '#')}" target="_blank" class="news-link">
                            📖 Read Full Article
                        </a>
                    </div>
                    """, unsafe_allow_html=True)
        
        # News Features Tips
        st.markdown("""
        <div class="welcome-card">
            <h3>📰 News Features</h3>
            <div class="feature-list">
                <div class="feature-item">🔍 Real-time news from NewsAPI.org</div>
                <div class="feature-item">📊 Contextual analysis based on stock performance</div>
                <div class="feature-item">🌐 Multiple news sources and fallbacks</div>
                <div class="feature-item">⚡ Fast loading with error handling</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    else:
        # Welcome message
        st.markdown("""
        <div class="welcome-card">
            <h2>🚀 Welcome to Portfolio Analyzer Pro</h2>
            <p>Your comprehensive stock portfolio analysis tool with real-time data and insights.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-list">
            <h3>🎯 What This Tool Does:</h3>
            <div class="feature-item">📊 Analyzes your stock portfolio from CSV files</div>
            <div class="feature-item">💰 Calculates XIRR for each holding</div>
            <div class="feature-item">📈 Tracks portfolio performance over time</div>
            <div class="feature-item">📰 Fetches real-time news for your stocks</div>
            <div class="feature-item">🌍 Supports multiple currencies (USD, INR, SGD)</div>
            <div class="feature-item">📊 Handles stock splits automatically</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-list">
            <h3>🚀 How to Get Started:</h3>
            <div class="feature-item">1. Upload your CSV files in the sidebar (or use demo mode)</div>
            <div class="feature-item">2. Click "Run Portfolio Analysis" in the sidebar</div>
            <div class="feature-item">3. Wait for the analysis to complete</div>
            <div class="feature-item">4. Explore your portfolio insights</div>
            <div class="feature-item">5. Get real-time news for your stocks</div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="feature-list">
            <h3>📁 Your Portfolio Data Files:</h3>
            <div class="feature-item">• Stock_trading_2023.csv (31 trades)</div>
            <div class="feature-item">• Stock_trading_2024.csv (365 trades)</div>
            <div class="feature-item">• Stock_trading_2025.csv (126 trades)</div>
            <div class="feature-item">• Total: 522 trades across 16 symbols</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Data preview
        st.markdown("### 📁 Your Portfolio Data Preview")
        try:
            # Try to load user's actual data
            sample_data = pd.read_csv('Stock_trading_2023.csv', nrows=5)
            st.dataframe(sample_data, use_container_width=True)
            st.success("📊 Your actual portfolio data is loaded and ready for analysis!")
            st.info("💡 Click 'Run Portfolio Analysis' to analyze your real portfolio data!")
        except:
            st.info("📊 Your portfolio data files not found. Please upload them or use demo mode.")
            
            # Show demo mode option
            if st.button("🎯 Create Demo Data", use_container_width=True):
                st.info("🔄 Creating demo data...")
                create_demo_data()
                st.success("✅ Demo data created! Click 'Run Portfolio Analysis' now.")
                st.rerun()

if __name__ == "__main__":
    main() 