import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from portfolio_analyzer import PortfolioAnalyzer
import numpy as np
from datetime import datetime
import time

# Page configuration
st.set_page_config(
    page_title="Portfolio Analyzer",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Modern CSS with better styling
st.markdown("""
<style>
    /* Modern Color Scheme */
    :root {
        --primary-color: #6366f1;
        --secondary-color: #8b5cf6;
        --success-color: #10b981;
        --warning-color: #f59e0b;
        --danger-color: #ef4444;
        --dark-bg: #0f172a;
        --card-bg: #1e293b;
        --text-primary: #f8fafc;
        --text-secondary: #cbd5e1;
        --border-color: #334155;
    }
    
    /* Global Styles */
    .main .block-container {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
        color: var(--text-primary);
    }
    
    .stApp {
        background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
    }
    
    /* Header Styling */
    .main-header {
        font-size: 3.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-align: center;
        margin-bottom: 3rem;
        text-shadow: 0 4px 8px rgba(0,0,0,0.3);
    }
    
    /* Card Styling */
    .metric-card {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 1.5rem;
        border-radius: 1rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
        transition: all 0.3s ease;
    }
    
    .metric-card:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 40px rgba(0,0,0,0.4);
    }
    
    /* Info Box */
    .info-box {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        padding: 2rem;
        border-radius: 1rem;
        border: 1px solid var(--border-color);
        box-shadow: 0 8px 32px rgba(0,0,0,0.3);
        backdrop-filter: blur(10px);
    }
    
    /* Button Styling */
    .stButton > button {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border: none;
        border-radius: 0.75rem;
        padding: 0.75rem 1.5rem;
        font-weight: 600;
        transition: all 0.3s ease;
        box-shadow: 0 4px 16px rgba(99, 102, 241, 0.3);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 24px rgba(99, 102, 241, 0.4);
    }
    
    /* Sidebar Styling */
    .css-1d391kg {
        background: linear-gradient(180deg, #1e293b 0%, #334155 100%);
    }
    
    /* Dataframe Styling */
    .dataframe {
        background: linear-gradient(135deg, #1e293b 0%, #334155 100%);
        border-radius: 0.75rem;
        border: 1px solid var(--border-color);
    }
    
    /* Chart Styling */
    .js-plotly-plot {
        border-radius: 1rem;
        overflow: hidden;
    }
    
    /* Text Colors */
    .positive {
        color: #10b981;
        font-weight: 600;
    }
    
    .negative {
        color: #ef4444;
        font-weight: 600;
    }
    
    /* Section Headers */
    h1, h2, h3 {
        color: var(--text-primary);
        font-weight: 700;
    }
    
    /* Metric Values */
    .metric-value {
        font-size: 1.5rem;
        font-weight: 700;
        color: var(--text-primary);
    }
    
    /* Loading Animation */
    .loading {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid rgba(255,255,255,.3);
        border-radius: 50%;
        border-top-color: #6366f1;
        animation: spin 1s ease-in-out infinite;
    }
    
    @keyframes spin {
        to { transform: rotate(360deg); }
    }
    
    /* Custom Scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1e293b;
    }
    
    ::-webkit-scrollbar-thumb {
        background: linear-gradient(135deg, #6366f1, #8b5cf6);
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: linear-gradient(135deg, #8b5cf6, #6366f1);
    }
</style>
""", unsafe_allow_html=True)

def main():
    # Header with modern gradient
    st.markdown('<h1 class="main-header">🚀 Portfolio Analyzer Pro</h1>', unsafe_allow_html=True)
    
    # Sidebar with modern styling
    with st.sidebar:
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                    padding: 1.5rem; border-radius: 1rem; margin-bottom: 2rem;">
            <h3 style="color: #f8fafc; margin-bottom: 1rem;">⚙️ Settings</h3>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("###  Data Files")
        
        # Check if files exist
        import os
        files_exist = all(os.path.exists(f) for f in ['Stock_trading_2023.csv', 'Stock_trading_2024.csv', 'Stock_trading_2025.csv'])
        
        if files_exist:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                        padding: 1rem; border-radius: 0.75rem; color: white; font-weight: 600;">
                 All CSV files found!
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                        padding: 1rem; border-radius: 0.75rem; color: white; font-weight: 600;">
                ❌ Some CSV files are missing
            </div>
            """, unsafe_allow_html=True)
            st.info("Please ensure all three CSV files are in the current directory")
            return
        
        # Modern analysis button
        st.markdown("###  Analysis")
        if st.button(" Run Portfolio Analysis", type="primary", use_container_width=True):
            with st.spinner("🔄 Analyzing portfolio data..."):
                try:
                    # Initialize analyzer
                    analyzer = PortfolioAnalyzer()
                    
                    # Run analysis
                    file_paths = ['Stock_trading_2023.csv', 'Stock_trading_2024.csv', 'Stock_trading_2025.csv']
                    analyzer.run_complete_analysis(file_paths)
                    
                    # Store in session state
                    st.session_state.analyzer = analyzer
                    st.session_state.analysis_complete = True
                    
                    st.markdown("""
                    <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                                padding: 1rem; border-radius: 0.75rem; color: white; font-weight: 600; text-align: center;">
                        ✅ Analysis completed successfully!
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Force rerun to show the main content
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Error during analysis: {str(e)}")
                    st.session_state.analysis_complete = False
    
    # Main content
    if 'analysis_complete' in st.session_state and st.session_state.analysis_complete and hasattr(st.session_state, 'analyzer'):
        analyzer = st.session_state.analyzer
        
        # Overview Section with modern cards
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                    padding: 2rem; border-radius: 1rem; margin-bottom: 2rem; border: 1px solid #475569;">
            <h2 style="color: #f8fafc; margin-bottom: 1.5rem; text-align: center;">📊 Portfolio Overview</h2>
        </div>
        """, unsafe_allow_html=True)
        
        # Modern metric cards
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            total_holdings = len(analyzer.holdings)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%); 
                        padding: 1.5rem; border-radius: 1rem; text-align: center; color: white;">
                <h3 style="margin: 0; font-size: 2rem; font-weight: 800;">{total_holdings}</h3>
                <p style="margin: 0; opacity: 0.9;">Total Holdings</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            total_trades = len(analyzer.all_trades)
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                        padding: 1.5rem; border-radius: 1rem; text-align: center; color: white;">
                <h3 style="margin: 0; font-size: 2rem; font-weight: 800;">{total_trades}</h3>
                <p style="margin: 0; opacity: 0.9;">Total Trades</p>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if hasattr(analyzer, 'portfolio_values') and not analyzer.portfolio_values.empty:
                latest_value = analyzer.portfolio_values['Value_USD'].iloc[-1]
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); 
                            padding: 1.5rem; border-radius: 1rem; text-align: center; color: white;">
                    <h3 style="margin: 0; font-size: 1.5rem; font-weight: 800;">${latest_value:,.0f}</h3>
                    <p style="margin: 0; opacity: 0.9;">Portfolio Value</p>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown("""
                <div style="background: linear-gradient(135deg, #6b7280 0%, #4b5563 100%); 
                            padding: 1.5rem; border-radius: 1rem; text-align: center; color: white;">
                    <h3 style="margin: 0; font-size: 1.5rem; font-weight: 800;">Calculating...</h3>
                    <p style="margin: 0; opacity: 0.9;">Portfolio Value</p>
                </div>
                """, unsafe_allow_html=True)
        
        with col4:
            if hasattr(analyzer, 'xirr_results') and analyzer.xirr_results:
                avg_xirr = np.mean(list(analyzer.xirr_results.values())) * 100
                color = "#10b981" if avg_xirr > 0 else "#ef4444"
                st.markdown(f"""
                <div style="background: linear-gradient(135deg, {color} 0%, {color}dd 100%); 
                            padding: 1.5rem; border-radius: 1rem; text-align: center; color: white;">
                    <h3 style="margin: 0; font-size: 2rem; font-weight: 800;">{avg_xirr:.1f}%</h3>
                    <p style="margin: 0; opacity: 0.9;">Avg XIRR</p>
                </div>
                """, unsafe_allow_html=True)
        
        # Holdings Table with modern styling
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                    padding: 2rem; border-radius: 1rem; margin-bottom: 2rem; border: 1px solid #475569;">
            <h2 style="color: #f8fafc; margin-bottom: 1.5rem; text-align: center;">💼 Current Holdings</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if not analyzer.holdings.empty:
            holdings_df = analyzer.holdings.copy()
            
            # Add current prices and values
            current_prices = []
            current_values = []
            
            for _, holding in holdings_df.iterrows():
                symbol = holding['Symbol']
                if symbol in analyzer.historical_prices and not analyzer.historical_prices[symbol].empty:
                    current_price = analyzer.historical_prices[symbol]['Close'].iloc[-1]
                    current_prices.append(current_price)
                    current_values.append(holding['Quantity'] * current_price)
                else:
                    current_prices.append(0)
                    current_values.append(0)
            
            holdings_df['Current_Price'] = current_prices
            holdings_df['Current_Value'] = current_values
            holdings_df['Unrealized_PL'] = holdings_df['Current_Value'] - holdings_df['Total_Invested']
            holdings_df['Unrealized_PL_Pct'] = (holdings_df['Unrealized_PL'] / holdings_df['Total_Invested']) * 100
            
            # Format the display
            display_df = holdings_df[['Symbol', 'Currency', 'Quantity', 'Avg_Price', 'Current_Price', 
                                   'Total_Invested', 'Current_Value', 'Unrealized_PL', 'Unrealized_PL_Pct']].copy()
            
            display_df['Total_Invested'] = display_df['Total_Invested'].apply(lambda x: f"${x:,.2f}")
            display_df['Current_Value'] = display_df['Current_Value'].apply(lambda x: f"${x:,.2f}")
            display_df['Unrealized_PL'] = display_df['Unrealized_PL'].apply(lambda x: f"${x:,.2f}")
            display_df['Unrealized_PL_Pct'] = display_df['Unrealized_PL_Pct'].apply(lambda x: f"{x:.2f}%")
            display_df['Avg_Price'] = display_df['Avg_Price'].apply(lambda x: f"${x:.2f}")
            display_df['Current_Price'] = display_df['Current_Price'].apply(lambda x: f"${x:.2f}")
            
            # Modern dataframe styling
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                        padding: 1.5rem; border-radius: 1rem; border: 1px solid #475569;">
            """, unsafe_allow_html=True)
            st.dataframe(display_df, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Portfolio Performance Chart with modern styling
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                    padding: 2rem; border-radius: 1rem; margin-bottom: 2rem; border: 1px solid #475569;">
            <h2 style="color: #f8fafc; margin-bottom: 1.5rem; text-align: center;">📈 Portfolio Performance</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if hasattr(analyzer, 'portfolio_values') and not analyzer.portfolio_values.empty:
            fig = go.Figure()
            
            fig.add_trace(go.Scatter(
                x=analyzer.portfolio_values['Date'],
                y=analyzer.portfolio_values['Value_USD'],
                mode='lines',
                name='Portfolio Value (USD)',
                line=dict(color='#6366f1', width=4),
                fill='tonexty',
                fillcolor='rgba(99, 102, 241, 0.1)'
            ))
            
            fig.update_layout(
                title=dict(
                    text="Portfolio Value Over Time",
                    font=dict(size=20, color='#f8fafc')
                ),
                xaxis=dict(
                    title="Date",
                    gridcolor='#475569',
                    color='#cbd5e1'
                ),
                yaxis=dict(
                    title="Value (USD)",
                    gridcolor='#475569',
                    color='#cbd5e1'
                ),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                hovermode='x unified',
                height=500,
                font=dict(color='#f8fafc')
            )
            
            st.plotly_chart(fig, use_container_width=True)
        
        # XIRR Analysis
        st.header("🎯 XIRR Analysis")
        
        if hasattr(analyzer, 'xirr_results') and analyzer.xirr_results:
            xirr_data = []
            for symbol, xirr_rate in analyzer.xirr_results.items():
                xirr_data.append({
                    'Symbol': symbol,
                    'XIRR': xirr_rate * 100
                })
            
            xirr_df = pd.DataFrame(xirr_data)
            xirr_df = xirr_df.sort_values('XIRR', ascending=False)
            
            # Create bar chart
            fig = px.bar(
                xirr_df, 
                x='Symbol', 
                y='XIRR',
                title="XIRR by Symbol",
                color='XIRR',
                color_continuous_scale='RdYlGn'
            )
            
            fig.update_layout(height=500)
            st.plotly_chart(fig, use_container_width=True)
            
            # XIRR table
            st.subheader("XIRR Details")
            xirr_df['XIRR'] = xirr_df['XIRR'].apply(lambda x: f"{x:.2f}%")
            st.dataframe(xirr_df, use_container_width=True)
        
        # Stock Splits Information
        st.header("📊 Stock Splits")
        
        splits_data = []
        for symbol, splits in analyzer.stock_splits.items():
            if not splits.empty:
                for date, ratio in splits.items():
                    splits_data.append({
                        'Symbol': symbol,
                        'Split Date': date.strftime('%Y-%m-%d'),
                        'Split Ratio': f"1:{ratio:.2f}"
                    })
        
        if splits_data:
            splits_df = pd.DataFrame(splits_data)
            st.dataframe(splits_df, use_container_width=True)
        else:
            st.info("No stock splits found in the analyzed period.")
        
        # News Section
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                    padding: 2rem; border-radius: 1rem; margin-bottom: 2rem; border: 1px solid #475569;">
            <h2 style="color: #f8fafc; margin-bottom: 1.5rem; text-align: center;">�� Latest Market News & Analysis</h2>
        </div>
        """, unsafe_allow_html=True)
        
        if not analyzer.holdings.empty:
            col1, col2 = st.columns([2, 1])
            
            with col1:
                selected_symbol = st.selectbox(
                    "Select a stock symbol to view latest news and analysis:",
                    analyzer.holdings['Symbol'].unique(),
                    help="Choose any stock from your portfolio to get the latest news, market analysis, and trading insights"
                )
            
            with col2:
                st.markdown("<br>", unsafe_allow_html=True)
                if st.button("🚀 Get Latest News & Analysis", type="primary", use_container_width=True):
                    with st.spinner("📡 Fetching latest news and market analysis..."):
                        news = analyzer.get_latest_news(selected_symbol)
                        
                        if news:
                            st.markdown(f"""
                            <div style="background: linear-gradient(135deg, #10b981 0%, #059669 100%); 
                                        padding: 1rem; border-radius: 0.75rem; color: white; font-weight: 600; text-align: center; margin-bottom: 1rem;">
                                ✅ Found {len(news)} news articles and market insights for {selected_symbol}
                            </div>
                            """, unsafe_allow_html=True)
                            
                            for i, article in enumerate(news[:5]):
                                # Color code based on publisher and content type
                                if "Portfolio Analyzer" in article.get('publisher', ''):
                                    if "Technical Analysis" in article.get('title', ''):
                                        bg_color = "linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%)"
                                    elif "Performance" in article.get('title', ''):
                                        bg_color = "linear-gradient(135deg, #f59e0b 0%, #d97706 100%)"
                                    elif "Trend" in article.get('title', ''):
                                        bg_color = "linear-gradient(135deg, #06b6d4 0%, #0891b2 100%)"
                                    else:
                                        bg_color = "linear-gradient(135deg, #6366f1 0%, #8b5cf6 100%)"
                                else:
                                    bg_color = "linear-gradient(135deg, #1e293b 0%, #334155 100%)"
                                
                                with st.expander(f"📰 {article.get('title', 'No title')}", expanded=(i==0)):
                                    st.markdown(f"""
                                    <div style="background: {bg_color}; padding: 1.5rem; border-radius: 0.75rem; margin-bottom: 1rem;">
                                        <p style="margin-bottom: 0.5rem;"><strong>📅 Published:</strong> {article.get('published', 'Unknown')}</p>
                                        <p style="margin-bottom: 0.5rem;"><strong>📰 Publisher:</strong> {article.get('publisher', 'Unknown')}</p>
                                        <p style="margin-bottom: 0.5rem;"><strong>📝 Analysis:</strong> {article.get('summary', 'No summary available')}</p>
                                    </div>
                                    """, unsafe_allow_html=True)
                                    
                                    if article.get('link'):
                                        st.markdown(f"""
                                        <div style="text-align: center; margin-top: 1rem;">
                                            <a href="{article['link']}" target="_blank" style="
                                                background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
                                                color: white;
                                                padding: 0.75rem 1.5rem;
                                                border-radius: 0.5rem;
                                                text-decoration: none;
                                                font-weight: 600;
                                                display: inline-block;
                                                transition: all 0.3s ease;">
                                                🔗 Read Full Article & Charts
                                            </a>
                                        </div>
                                        """, unsafe_allow_html=True)
                        else:
                            st.markdown("""
                            <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                                        padding: 1rem; border-radius: 0.75rem; color: white; font-weight: 600; text-align: center;">
                                ❌ No news available for this symbol
                            </div>
                            """, unsafe_allow_html=True)
            
            # Add enhanced news tips
            st.markdown("""
            <div style="background: linear-gradient(135deg, rgba(99, 102, 241, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%); 
                        padding: 1.5rem; border-radius: 0.75rem; border: 1px solid #6366f1; margin-top: 1rem;">
                <h4 style="color: #6366f1; margin-bottom: 1rem;">💡 Enhanced News & Analysis Features:</h4>
                <ul style="color: #cbd5e1; margin: 0;">
                    <li>📰 <strong>Real-time news</strong> from Yahoo Finance and other sources</li>
                    <li>📊 <strong>Price-based analysis</strong> with technical insights</li>
                    <li>📈 <strong>Weekly & monthly trends</strong> for comprehensive analysis</li>
                    <li>🔗 <strong>Direct links</strong> to Yahoo Finance charts and data</li>
                    <li>📅 <strong>Publication dates</strong> and detailed summaries</li>
                    <li>🎯 <strong>Contextual insights</strong> based on your portfolio data</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        # Trade History
        st.header("📋 Trade History")
        
        if not analyzer.all_trades.empty:
            # Filter options
            col1, col2 = st.columns(2)
            
            with col1:
                selected_symbol_filter = st.selectbox(
                    "Filter by Symbol:",
                    ['All'] + list(analyzer.all_trades['Symbol'].unique())
                )
            
            with col2:
                selected_currency_filter = st.selectbox(
                    "Filter by Currency:",
                    ['All'] + list(analyzer.all_trades['Currency'].unique())
                )
            
            # Apply filters
            filtered_trades = analyzer.all_trades.copy()
            
            if selected_symbol_filter != 'All':
                filtered_trades = filtered_trades[filtered_trades['Symbol'] == selected_symbol_filter]
            
            if selected_currency_filter != 'All':
                filtered_trades = filtered_trades[filtered_trades['Currency'] == selected_currency_filter]
            
            # Display trades
            display_trades = filtered_trades[['Date/Time', 'Symbol', 'Currency', 'Quantity', 'T. Price', 'C. Price', 'Proceeds']].copy()
            display_trades['Date/Time'] = display_trades['Date/Time'].dt.strftime('%Y-%m-%d %H:%M')
            display_trades['T. Price'] = display_trades['T. Price'].apply(lambda x: f"${x:.2f}")
            display_trades['C. Price'] = display_trades['C. Price'].apply(lambda x: f"${x:.2f}")
            display_trades['Proceeds'] = display_trades['Proceeds'].apply(lambda x: f"${x:,.2f}")
            
            st.dataframe(display_trades, use_container_width=True)
        
        # Currency Analysis
        st.header("💱 Currency Analysis")
        
        if not analyzer.all_trades.empty:
            currency_summary = analyzer.all_trades.groupby('Currency').agg({
                'Proceeds': 'sum',
                'Symbol': 'count'
            }).reset_index()
            
            currency_summary.columns = ['Currency', 'Total_Proceeds', 'Trade_Count']
            currency_summary['Total_Proceeds'] = currency_summary['Total_Proceeds'].apply(lambda x: f"${x:,.2f}")
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("Trades by Currency")
                fig = px.pie(currency_summary, values='Trade_Count', names='Currency', title="Trade Distribution by Currency")
                st.plotly_chart(fig, use_container_width=True)
            
            with col2:
                st.subheader("Currency Summary")
                st.dataframe(currency_summary, use_container_width=True)
    
    else:
        # Debug information
        st.markdown("""
        <div style="background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); 
                    padding: 1rem; border-radius: 0.75rem; color: white; font-weight: 600; text-align: center; margin-bottom: 1rem;">
            🔍 Debug Info: Analysis not complete or analyzer not found
        </div>
        """, unsafe_allow_html=True)
        
        # Show session state info
        st.write("Session State:", st.session_state)
        
        # Modern welcome message
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                    padding: 3rem; border-radius: 1.5rem; border: 1px solid #475569; 
                    box-shadow: 0 8px 32px rgba(0,0,0,0.3); margin-bottom: 3rem;">
            <h2 style="color: #f8fafc; margin-bottom: 2rem; text-align: center; font-size: 2.5rem;">
                🚀 Welcome to Portfolio Analyzer Pro
            </h2>
            <p style="color: #cbd5e1; font-size: 1.1rem; margin-bottom: 2rem; text-align: center;">
                Your comprehensive investment analysis platform with advanced features and modern insights.
            </p>
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
                <div style="background: rgba(99, 102, 241, 0.1); padding: 1.5rem; border-radius: 0.75rem; border: 1px solid #6366f1;">
                    <h4 style="color: #6366f1; margin-bottom: 1rem;">📊 Portfolio Overview</h4>
                    <p style="color: #cbd5e1;">Real-time portfolio analysis with current holdings and performance metrics</p>
                </div>
                <div style="background: rgba(16, 185, 129, 0.1); padding: 1.5rem; border-radius: 0.75rem; border: 1px solid #10b981;">
                    <h4 style="color: #10b981; margin-bottom: 1rem;">📈 Performance Tracking</h4>
                    <p style="color: #cbd5e1;">Historical performance charts and XIRR calculations</p>
                </div>
                <div style="background: rgba(245, 158, 11, 0.1); padding: 1.5rem; border-radius: 0.75rem; border: 1px solid #f59e0b;">
                    <h4 style="color: #f59e0b; margin-bottom: 1rem;">🎯 Advanced Analytics</h4>
                    <p style="color: #cbd5e1;">Stock split adjustments and multi-currency analysis</p>
                </div>
                <div style="background: rgba(139, 92, 246, 0.1); padding: 1.5rem; border-radius: 0.75rem; border: 1px solid #8b5cf6;">
                    <h4 style="color: #8b5cf6; margin-bottom: 1rem;">📰 Market News</h4>
                    <p style="color: #cbd5e1;">Latest news and insights for your holdings</p>
                </div>
            </div>
            <div style="text-align: center; padding: 2rem; background: rgba(99, 102, 241, 0.1); border-radius: 0.75rem; border: 1px solid #6366f1;">
                <h3 style="color: #f8fafc; margin-bottom: 1rem;">🚀 Ready to Analyze?</h3>
                <p style="color: #cbd5e1; font-size: 1.1rem;">
                    Click the <strong>"Run Portfolio Analysis"</strong> button in the sidebar to start your comprehensive portfolio analysis!
                </p>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Modern data preview
        st.markdown("""
        <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                    padding: 2rem; border-radius: 1rem; border: 1px solid #475569;">
            <h2 style="color: #f8fafc; margin-bottom: 1.5rem; text-align: center;">📋 Data Preview</h2>
        </div>
        """, unsafe_allow_html=True)
        
        try:
            sample_df = pd.read_csv('Stock_trading_2023.csv')
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                        padding: 1.5rem; border-radius: 1rem; border: 1px solid #475569;">
            """, unsafe_allow_html=True)
            st.write("Sample data from 2023:")
            st.dataframe(sample_df.head(10), use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)
        except:
            st.markdown("""
            <div style="background: linear-gradient(135deg, #1e293b 0%, #334155 100%); 
                        padding: 1.5rem; border-radius: 1rem; border: 1px solid #475569; text-align: center;">
                <p style="color: #cbd5e1;">Sample data will be displayed once the analysis is run.</p>
            </div>
            """, unsafe_allow_html=True)

if __name__ == "__main__":
    main() 