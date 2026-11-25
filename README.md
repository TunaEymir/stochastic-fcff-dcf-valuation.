# stochastic-fcff-dcf-valuation.
5-year FCFF Discounted Cash Flow (DCF) and Monte Carlo valuation engine for European equities (pilot: SAP SE), built with Python and Streamlit.
An automated **5-year Discounted Cash Flow (FCFF)** and **Monte Carlo simulation** engine for valuing publicly listed European equities, piloted on **SAP SE (`SAP.DE`)**.

> **Disclaimer:** This project is an educational and analytical modeling tool built for financial analysis and portfolio demonstration purposes. It does not constitute investment advice.

---

## Key Features
- **Automated Financial Data Ingestion:** Pulls historical income statement, balance sheet, and cash flow statement items via Python data pipelines with missing-value handling and sanity checks.
- **5-Year FCFF Projection:** Projects Free Cash Flow to the Firm across a 5-year explicit forecast horizon ($t = 1 \dots 5$).
- **WACC & CAPM Engine:** Computes cost of equity via CAPM and after-tax cost of debt weighted by market/balance-sheet capital structure.
- **Terminal Value & Equity Bridge:** Calculates terminal value via the Gordon Growth Model and bridges from **Enterprise Value (EV)** to **Implied Share Price**.
- **Monte Carlo Simulation:** Runs 10,000 vectorized iterations over key assumptions to produce an implied valuation distribution (P10 / P50 / P90) rather than a single point estimate.
- **Sensitivity Analysis:** Evaluates implied share price sensitivity across WACC and terminal growth rate ($g$) scenarios.

---

## Financial Methodology

### 1. Free Cash Flow to the Firm (FCFF)
For each projection year $t \in \{1, 2, 3, 4, 5\}$:

$$\text{FCFF}_t = \text{EBIT}_t \times (1 - \tau) + \text{DA}_t - \text{CapEx}_t - \Delta \text{NWC}_t$$

- **Revenue Growth:** Anchored on historical growth and tapered toward long-term equilibrium over the 5-year horizon.
- **Operating & Capital Items:** EBIT margin, Depreciation and Amortization ($\text{DA}$), Capital Expenditures ($\text{CapEx}$), and changes in Net Working Capital ($\Delta \text{NWC}$) are modeled using historical ratios/averages and sanity-checked against company disclosures.
- **Effective Tax Rate ($\tau$):** Derived from historical tax expense over pretax income, bounded within a realistic range (e.g., 15%–35%) to prevent distortion from one-off items.

### 2. Weighted Average Cost of Capital (WACC)

$$\text{WACC} = \left(\frac{E}{V} \times R_e\right) + \left(\frac{D}{V} \times R_d \times (1 - \tau)\right)$$

- **Cost of Equity ($R_e$):** Estimated using CAPM ($R_e = R_f + \beta \times \text{ERP}$), referencing European benchmark risk-free rates ($R_f$), equity beta ($\beta$), and European Equity Risk Premium ($\text{ERP}$).
- **Cost of Debt ($R_d$):** Estimated from interest expense relative to total debt, adjusted by the effective tax shield $(1 - \tau)$.
- **Capital Weights ($E/V$ and $D/V$):** Based on equity value ($E$) and total debt ($D$), where $V = E + D$.

### 3. Terminal Value & Equity Bridge
Using the Gordon Growth Model at year $5$ with long-term growth rate $g$:

$$\text{TV}_5 = \frac{\text{FCFF}_5 \times (1 + g)}{\text{WACC} - g}$$

$$\text{Enterprise Value (EV)} = \sum_{t=1}^{5} \frac{\text{FCFF}_t}{(1 + \text{WACC})^t} + \frac{\text{TV}_5}{(1 + \text{WACC})^5}$$

$$\text{Equity Value} = \text{EV} + \text{Cash and Short-Term Investments} - \text{Total Debt}$$

$$\text{Implied Share Price} = \frac{\text{Equity Value}}{\text{Diluted Shares Outstanding}}$$

### 4. Monte Carlo & Sensitivity Framework
- **Monte Carlo:** Key drivers (such as revenue growth, operating margin, and WACC) are sampled across $10,000$ iterations to generate a probability distribution of implied share prices and percentiles (P10, P50, P90).
- **Sensitivity Grid:** A two-way table/heatmap shows how implied value shifts across WACC and terminal growth ($g$) assumptions.

---

## Project Structure

```text
stochastic-fcff-dcf-valuation/
├── data/                  # Sample/cached datasets and verification notes
├── src/
│   ├── __init__.py
│   ├── data_loader.py     # Financial statement retrieval & cleaning
│   ├── financials.py      # FCFF, WACC, TV, and equity bridge logic
│   ├── monte_carlo.py     # Vectorized Monte Carlo simulation
│   └── visualizer.py      # Distribution plots & sensitivity tables
├── tests/                 # Unit tests for valuation & edge cases
├── app.py                 # Interactive Streamlit dashboard (optional/next stage)
├── requirements.txt
└── README.md
