import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from scipy.sparse import csr_matrix

# ----------------------------------------------------------------------
# Load Dataset
# ----------------------------------------------------------------------
data_path = r"C:\Users\Shreya Patil\Desktop\INTERNSHIPS\intrainz internship\Data_science_internship\OnlineRetail.xlsx"
df = pd.read_excel(data_path, sheet_name="OnlineRetail")

# ----------------------------------------------------------------------
# Data Cleaning
# ----------------------------------------------------------------------
# Remove missing CustomerID
df.dropna(subset=['CustomerID'], inplace=True)

# Retain positive transactions only
df = df[(df['Quantity'] > 0) & (df['UnitPrice'] > 0)]

# Convert CustomerID to integer
df['CustomerID'] = df['CustomerID'].astype(int)

# ----------------------------------------------------------------------
# Create User-Item Matrix
# ----------------------------------------------------------------------
user_item_matrix = df.pivot_table(
    index='CustomerID',
    columns='StockCode',
    values='Quantity',
    aggfunc='sum',
    fill_value=0
)

# Sparse matrix for performance
sparse_matrix = csr_matrix(user_item_matrix)

# ----------------------------------------------------------------------
# Compute Customer Similarity (Cosine Similarity)
# ----------------------------------------------------------------------
customer_similarity = cosine_similarity(sparse_matrix)
customer_similarity_df = pd.DataFrame(
    customer_similarity,
    index=user_item_matrix.index,
    columns=user_item_matrix.index
)

# ----------------------------------------------------------------------
# Recommendation Function
# ----------------------------------------------------------------------
def recommend_products(customer_id, num_recommendations=5):
    """
    Recommend products for a customer based on similar users' purchase behavior.
    
    Recommendations follow a collaborative filtering approach:
    1. Identify top similar customers.
    2. Extract products frequently purchased by them.
    3. Return top-N recommended StockCodes + Descriptions.
    """
    
    # Validate customer
    if customer_id not in customer_similarity_df.index:
        return "Customer ID not found in database."
    
    # Fetch top 5 most similar customers (skip self)
    similar_customers = (
        customer_similarity_df[customer_id]
        .sort_values(ascending=False)
        .iloc[1:6]
        .index
    )
    
    # Get purchase history of similar customers
    similar_purchases = df[df['CustomerID'].isin(similar_customers)]
    
    # Rank products by purchase frequency
    top_products = (
        similar_purchases['StockCode']
        .value_counts()
        .index[:num_recommendations]
        .tolist()
    )
    
    # Return unique product descriptions
    recommendations = (
        df[df['StockCode'].isin(top_products)][['StockCode', 'Description']]
        .drop_duplicates()
        .reset_index(drop=True)
    )
    
    return recommendations

# ----------------------------------------------------------------------
# Example Usage
# ----------------------------------------------------------------------
sample_customer = df['CustomerID'].iloc[0]  # Pick first customer
recommendations = recommend_products(sample_customer)

print(recommendations)
