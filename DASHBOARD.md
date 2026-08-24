# Airline Dashboard 📊

The Airline RAG System includes an interactive **AI/BI Lakeview Dashboard** with 3 pages:

## 📈 Dashboard Pages

### 1. **Price Metrics**
* Total flights tracked
* Average flight prices
* Business vs Economy premium ratio
* Price by airline, class, and stops
* Price trends vs days before departure

### 2. **Performance Metrics**
* Top 10 routes by revenue potential
* Top 10 routes by price vs volume
* Airline positioning (volume vs price by class)
* Time-of-day pricing analysis

### 3. **Predictions**
* ML price predictions vs actual prices
* Price band distribution (₹0-5K, ₹5K-10K, ₹10K-20K, ₹20K+)
* Statistical summary (quartiles, median)
* Price distribution by class (box plots)

---

## 🔗 Access Options

You have **two ways** to share or access this dashboard:

### **Option 1: Make Dashboard Public** (Easiest)

**Best for:** Sharing with external users or embedding on websites

1. **Open the dashboard** in Databricks:
   ```
   /Users/jeanfred4@gmail.com/Airline Dashboard.lvdash.json
   ```

2. **Click "Share" button** (top right)

3. **Enable "Public Access"**:
   * Toggle **"Allow public access"** ON
   * Copy the **public URL**

4. **Share the URL** - anyone with the link can view (no login required)

⚠️ **Note**: The dashboard will be **read-only** for public viewers

---

### **Option 2: Export Dashboard to Git** (Version Control)

**Best for:** Version control, collaboration, backup

#### **Method A: Manual Export (Recommended)**

1. **Open the dashboard** in Databricks

2. **Click the "⋮" menu** (top right) → **"Download"**

3. **Save the `.lvdash.json` file**

4. **Add it to this Git repo**:
   ```bash
   # Copy the downloaded file to your repo
   cp ~/Downloads/Airline\ Dashboard.lvdash.json ./Airline_Dashboard.lvdash.json
   
   # Commit and push
   git add Airline_Dashboard.lvdash.json
   git commit -m "Add airline dashboard"
   git push origin main
   ```

#### **Method B: Copy Dashboard File**

The dashboard source file is at:
```
/Users/jeanfred4@gmail.com/Airline Dashboard.lvdash.json
```

**In Databricks Repos**, you can copy it:
```bash
cp "/Workspace/Users/jeanfred4@gmail.com/Airline Dashboard.lvdash.json" .
```

---

## 📂 Dashboard Data Sources

The dashboard queries these Unity Catalog tables:

* `airlines.gold_schema.gold_route_level_analysis`
* `airlines.gold_schema.gold_route_revenue_potential`
* `airlines.gold_schema.gold_class_level_analysis`
* `airlines.gold_schema.gold_airline_performance`
* `airlines.gold_schema.gold_price_vs_days_left`
* `airlines.gold_schema.gold_time_of_day_pricing`
* `airlines.silver_gold.flight_price_predictions`
* `airlines.silver_gold.silver_flights_data`

---

## 🔧 Recreating the Dashboard

If you want to **recreate the dashboard** in another workspace:

1. **Set up the data pipeline** (see `setup_data.py`)

2. **Import the dashboard file**:
   * Go to **Dashboards** in Databricks
   * Click **"Create"** → **"Import Dashboard"**
   * Upload the `.lvdash.json` file

3. **Update data sources** if your catalog/schema names are different

---

## 💡 Recommendation

**Use Option 1 (Public Access)** for:
* Sharing with stakeholders
* Embedding in websites/portals
* Quick demo/preview links

**Use Option 2 (Git Export)** for:
* Backup and version control
* Tracking dashboard changes over time
* Sharing the dashboard definition with other Databricks users

---

## 🔗 Links

* **Live Dashboard**: [Airline Dashboard](#dashboard-2497054289407567)
* **Data Setup**: See `setup_data.py`
* **RAG System**: See `rag_system.py`
* **GitHub Repo**: [airline-rag-system](https://github.com/JeanAndre376/airline-rag-system)
