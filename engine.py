import pandas as pd

# -------------------------------
# LOAD DATA
# -------------------------------
def load_data(file):
    df = pd.read_csv(file,encoding="latin-1")
    return df


# -------------------------------
# CLEAN DATA
# -------------------------------
def clean_data(df):
    df = df.copy()

    # Drop missing critical values
    df = df.dropna(subset=[
        "Days for shipping (real)",
        "Days for shipment (scheduled)",
        "Late_delivery_risk"
    ])

    # Convert to numeric (safe)
    df["Days for shipping (real)"] = pd.to_numeric(df["Days for shipping (real)"], errors="coerce")
    df["Days for shipment (scheduled)"] = pd.to_numeric(df["Days for shipment (scheduled)"], errors="coerce")

    return df


# -------------------------------
# FEATURE ENGINEERING
# -------------------------------
def add_features(df):
    df = df.copy()

    # Delay Gap
    df["delay_gap"] = df["Days for shipping (real)"] - df["Days for shipment (scheduled)"]

    # Delivery Classification
    def classify(x):
        if x > 0:
            return "Delayed"
        elif x == 0:
            return "On-Time"
        else:
            return "Early"

    df["delivery_status_new"] = df["delay_gap"].apply(classify)

    return df


# -------------------------------
# KPI CALCULATIONS
# -------------------------------
def calculate_kpis(df):
    total = len(df)

    on_time = (df["delivery_status_new"] == "On-Time").sum()
    delayed = (df["delivery_status_new"] == "Delayed").sum()

    on_time_rate = (on_time / total) * 100
    avg_delay = df["delay_gap"].mean()
    risk_ratio = df["Late_delivery_risk"].mean()

    return {
        "on_time_rate": on_time_rate,
        "avg_delay": avg_delay,
        "risk_ratio": risk_ratio
    }


# -------------------------------
# ANALYSIS FUNCTIONS
# -------------------------------
def shipping_mode_analysis(df):
    return df.groupby("Shipping Mode").agg({
        "delay_gap": "mean",
        "Late_delivery_risk": "mean"
    }).sort_values(by="delay_gap")


def regional_analysis(df):
    return df.groupby(["Order Region"]).agg({
        "delay_gap": "mean",
        "Late_delivery_risk": "mean"
    }).sort_values(by="delay_gap")


def customer_analysis(df):
    return df.groupby("Customer Segment").agg({
        "delay_gap": "mean",
        "Late_delivery_risk": "mean"
    }).sort_values(by="delay_gap")

def late_risk_distribution(df):
    return df["Late_delivery_risk"].value_counts(normalize=True)


def marketplace_analysis(df):
    return df.groupby("Market").agg({
        "delay_gap": "mean",
        "Late_delivery_risk": "mean"
    }).sort_values(by="delay_gap")
