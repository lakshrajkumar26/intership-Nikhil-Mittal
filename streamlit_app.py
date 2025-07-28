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
        
        # Analysis button
        if st.button("🔍 Run Portfolio Analysis", use_container_width=True):
            with st.spinner("Analyzing portfolio data..."):
                try:
                    # Initialize analyzer
                    analyzer = PortfolioAnalyzer()
                    
                    # File paths (for demo, we'll use sample data)
                    file_paths = [
                        'Stock_trading_2023.csv',
                        'Stock_trading_2024.csv', 
                        'Stock_trading_2025.csv'
                    ]
                    
                    # Run analysis
                    success = analyzer.run_complete_analysis(file_paths)
                    
                    if success:
                        st.session_state.analyzer = analyzer
                        st.session_state.analysis_complete = True
                        st.success("✅ Analysis completed successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Analysis failed. Please check your data files.")
                        
                except Exception as e:
                    st.error(f"❌ Error during analysis: {e}")
        
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
            <div class="feature-item">1. Click "Run Portfolio Analysis" in the sidebar</div>
            <div class="feature-item">2. Wait for the analysis to complete</div>
            <div class="feature-item">3. Explore your portfolio insights</div>
            <div class="feature-item">4. Get real-time news for your stocks</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Data preview
        st.markdown("### 📁 Data Preview")
        try:
            # Try to load sample data
            sample_data = pd.read_csv('Stock_trading_2023.csv', nrows=5)
            st.dataframe(sample_data, use_container_width=True)
            st.info("📊 Sample data loaded. Click 'Run Portfolio Analysis' to start!")
        except:
            st.info("📊 Ready to analyze your portfolio data!")

if __name__ == "__main__":
    main() 