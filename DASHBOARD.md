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

### **Make Dashboard Public** 

1. **Open the dashboard in Databricks:**
   ```
   https://dbc-25119fb3-3329.cloud.databricks.com/dashboardsv3/01f1978c33611adaa8a000284459bbf7/published?o=7474658491942202
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


## 🔗 Links

* **Live Dashboard**: [Airline Dashboard](#dashboard-2497054289407567)
* **Data Setup**: See `setup_data.py`
* **RAG System**: See `rag_system.py`
* **GitHub Repo**: [airline-rag-system](https://github.com/JeanAndre376/airline-rag-system)
