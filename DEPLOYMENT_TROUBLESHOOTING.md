# 🔧 Deployment Troubleshooting Guide

## 🚨 Common Issues & Solutions

### **Issue: "Analysis failed. Please check your data files"**

**Causes:**
1. CSV files not uploaded to deployment platform
2. Incorrect file format
3. Missing required columns
4. File path issues

**Solutions:**

#### **Option 1: Upload Your Files**
1. Use the file uploader in the sidebar
2. Upload your 3 CSV files:
   - `Stock_trading_2023.csv`
   - `Stock_trading_2024.csv`
   - `Stock_trading_2025.csv`

#### **Option 2: Use Demo Mode**
1. Click "🎯 Create Demo Data" button
2. This will generate sample data automatically
3. Then click "Run Portfolio Analysis"

#### **Option 3: Check File Format**
Ensure your CSV files have these columns:
```
Trades, DataDiscriminator, Date/Time, Symbol, Currency, Quantity, T. Price, C. Price, Proceeds
```

### **Issue: "Module not found" errors**

**Solution:**
- Make sure `requirements.txt` is in your repository
- Check that all dependencies are listed correctly

### **Issue: App won't start**

**Solutions:**
1. **For Streamlit Cloud:**
   - Check that `streamlit_app.py` is the main file
   - Verify `.streamlit/config.toml` exists

2. **For Heroku:**
   - Ensure `Procfile` is present
   - Check `runtime.txt` for correct Python version

3. **For Railway/Render:**
   - Verify build and start commands are correct

### **Issue: News not loading**

**Solutions:**
1. Check internet connectivity
2. Verify API keys are set correctly
3. The app has fallback mechanisms - it should still work

---

## 🛠️ **Quick Fix Steps**

### **Step 1: Test Locally First**
```bash
python -m streamlit run streamlit_app.py
```

### **Step 2: Check File Structure**
```
your-repo/
├── streamlit_app.py
├── portfolio_analyzer.py
├── requirements.txt
├── .streamlit/config.toml
├── Procfile (for Heroku)
├── runtime.txt (for Heroku)
└── Your CSV files (optional)
```

### **Step 3: Verify Dependencies**
Make sure `requirements.txt` contains:
```
pandas>=1.5.0
numpy>=1.21.0
numpy_financial>=1.0.0
yfinance>=0.2.0
requests>=2.25.0
streamlit>=1.25.0
plotly>=5.0.0
python-dateutil>=2.8.0
beautifulsoup4>=4.10.0
lxml>=4.6.0
openpyxl>=3.0.0
```

### **Step 4: Test Demo Mode**
1. Deploy without CSV files
2. Use the demo mode feature
3. Verify the app works with generated data

---

## 📞 **Getting Help**

### **For Streamlit Cloud:**
- Check deployment logs in the web interface
- Verify file paths and dependencies
- Use the demo mode to test functionality

### **For Heroku:**
```bash
heroku logs --tail
```

### **For Railway/Render:**
- Check the deployment logs in the web interface
- Verify environment variables if needed

---

## ✅ **Success Checklist**

Your deployment is working when:
- [ ] App loads without errors
- [ ] File upload works (or demo mode works)
- [ ] Portfolio analysis completes
- [ ] Charts display correctly
- [ ] News fetching works
- [ ] All features are functional

---

## 🎯 **Pro Tips**

1. **Always test demo mode first** - it's the easiest way to verify functionality
2. **Use file upload** - more reliable than embedding files in deployment
3. **Check logs** - deployment platforms provide detailed error information
4. **Start simple** - get the basic app working before adding complex features

**Your Portfolio Analyzer should work perfectly once these issues are resolved! 🚀** 