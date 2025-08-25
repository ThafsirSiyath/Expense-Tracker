import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, date
import calendar
import os

# Set page config
st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        border-left: 4px solid #667eea;
    }
    .expense-card {
        border-left: 4px solid #e74c3c;
    }
    .income-card {
        border-left: 4px solid #27ae60;
    }
</style>
""", unsafe_allow_html=True)

class ExpenseTracker:
    def __init__(self):
        self.expense_file = "expenses.csv"
        self.categories = {
            'expense': ["Food", "Home", "Work", "Fun", "Transportation", "Shopping", "Healthcare", "Entertainment"],
            'income': ["Salary", "Freelance", "Business", "Investment", "Gift", "Other"]
        }
        
    def load_data(self):
        """Load data from CSV file"""
        if os.path.exists(self.expense_file):
            try:
                df = pd.read_csv(self.expense_file)
                df['date'] = pd.to_datetime(df['date'])
                return df
            except:
                return pd.DataFrame(columns=['name', 'amount', 'category', 'type', 'date'])
        return pd.DataFrame(columns=['name', 'amount', 'category', 'type', 'date'])
    
    def save_expense(self, name, amount, category, expense_type):
        """Save expense/income to CSV"""
        new_entry = {
            'name': name,
            'amount': amount,
            'category': category,
            'type': expense_type,
            'date': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        
        df = self.load_data()
        df = pd.concat([df, pd.DataFrame([new_entry])], ignore_index=True)
        df.to_csv(self.expense_file, index=False)
        return True
    
    def get_remaining_days(self):
        """Get remaining days in current month"""
        today = date.today()
        last_day = calendar.monthrange(today.year, today.month)[1]
        return last_day - today.day
    
    def get_monthly_summary(self, df):
        """Get current month summary"""
        current_month = datetime.now().month
        current_year = datetime.now().year
        
        monthly_df = df[
            (df['date'].dt.month == current_month) & 
            (df['date'].dt.year == current_year)
        ]
        
        total_income = monthly_df[monthly_df['type'] == 'income']['amount'].sum()
        total_expenses = monthly_df[monthly_df['type'] == 'expense']['amount'].sum()
        
        return monthly_df, total_income, total_expenses

def main():
    tracker = ExpenseTracker()
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1 style="color: white; text-align: center; margin: 0;">💰 Expense Tracker</h1>
        <p style="color: white; text-align: center; margin: 0;">Track your income and expenses efficiently</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state
    if 'budget' not in st.session_state:
        st.session_state.budget = 2000
    
    # Sidebar for adding expenses/income
    with st.sidebar:
        st.header("Add Transaction")
        
        # Transaction type
        transaction_type = st.selectbox("Type", ["expense", "income"])
        
        # Name input
        name = st.text_input("Description", placeholder=f"Enter {transaction_type} description")
        
        # Amount input
        amount = st.number_input("Amount ($)", min_value=0.01, step=0.01, format="%.2f")
        
        # Category selection
        categories = tracker.categories[transaction_type]
        category = st.selectbox("Category", categories)
        
        # Add button
        if st.button(f"Add {transaction_type.title()}", type="primary", use_container_width=True):
            if name and amount > 0:
                success = tracker.save_expense(name, amount, category, transaction_type)
                if success:
                    st.success(f"{transaction_type.title()} added successfully!")
                    st.rerun()
            else:
                st.error("Please fill in all fields with valid data!")
        
        st.divider()
        
        # Budget setting
        st.header("Monthly Budget")
        new_budget = st.number_input(
            "Set Budget ($)", 
            min_value=100.0, 
            value=float(st.session_state.budget),
            step=50.0,
            format="%.2f"
        )
        if st.button("Update Budget"):
            st.session_state.budget = new_budget
            st.success("Budget updated!")
    
    # Load data
    df = tracker.load_data()
    
    if len(df) == 0:
        st.info("📝 No transactions yet. Add your first transaction using the sidebar!")
        return
    
    # Get monthly summary
    monthly_df, total_income, total_expenses = tracker.get_monthly_summary(df)
    balance = total_income - total_expenses
    remaining_budget = st.session_state.budget - total_expenses
    remaining_days = tracker.get_remaining_days()
    
    # Main dashboard
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #333;">Balance</h3>
            <h2 style="margin: 5px 0; color: {'#27ae60' if balance >= 0 else '#e74c3c'};">${balance:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
        <div class="metric-card income-card">
            <h3 style="margin: 0; color: #333;">Income</h3>
            <h2 style="margin: 5px 0; color: #27ae60;">${total_income:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown(f"""
        <div class="metric-card expense-card">
            <h3 style="margin: 0; color: #333;">Expenses</h3>
            <h2 style="margin: 5px 0; color: #e74c3c;">${total_expenses:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown(f"""
        <div class="metric-card">
            <h3 style="margin: 0; color: #333;">Budget Left</h3>
            <h2 style="margin: 5px 0; color: {'#27ae60' if remaining_budget >= 0 else '#e74c3c'};">${remaining_budget:,.2f}</h2>
        </div>
        """, unsafe_allow_html=True)
    
    # Progress bar for budget
    st.subheader("📊 Budget Progress")
    budget_used = (total_expenses / st.session_state.budget) * 100 if st.session_state.budget > 0 else 0
    st.progress(min(budget_used / 100, 1.0))
    st.write(f"Used: {budget_used:.1f}% of budget | {remaining_days} days remaining this month")
    
    # Charts
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💸 Expenses by Category")
        if len(monthly_df[monthly_df['type'] == 'expense']) > 0:
            expense_by_category = monthly_df[monthly_df['type'] == 'expense'].groupby('category')['amount'].sum()
            fig_pie = px.pie(
                values=expense_by_category.values,
                names=expense_by_category.index,
                title="Expense Distribution"
            )
            fig_pie.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expenses to show")
    
    with col2:
        st.subheader("💰 Income vs Expenses")
        if len(monthly_df) > 0:
            # Daily trend
            daily_summary = monthly_df.groupby([monthly_df['date'].dt.date, 'type'])['amount'].sum().reset_index()
            daily_pivot = daily_summary.pivot(index='date', columns='type', values='amount').fillna(0)
            
            fig_line = go.Figure()
            if 'income' in daily_pivot.columns:
                fig_line.add_trace(go.Scatter(
                    x=daily_pivot.index,
                    y=daily_pivot['income'].cumsum(),
                    mode='lines+markers',
                    name='Cumulative Income',
                    line=dict(color='#27ae60')
                ))
            if 'expense' in daily_pivot.columns:
                fig_line.add_trace(go.Scatter(
                    x=daily_pivot.index,
                    y=daily_pivot['expense'].cumsum(),
                    mode='lines+markers',
                    name='Cumulative Expenses',
                    line=dict(color='#e74c3c')
                ))
            
            fig_line.update_layout(title="Monthly Trend", xaxis_title="Date", yaxis_title="Amount ($)")
            st.plotly_chart(fig_line, use_container_width=True)
        else:
            st.info("No data to show trend")
    
    # Recent transactions
    st.subheader("📋 Recent Transactions")
    
    # Filter options
    col1, col2, col3 = st.columns(3)
    with col1:
        filter_type = st.selectbox("Filter by type", ["All", "income", "expense"])
    with col2:
        filter_category = st.selectbox("Filter by category", ["All"] + tracker.categories['expense'] + tracker.categories['income'])
    with col3:
        show_count = st.selectbox("Show", [10, 25, 50, "All"])
    
    # Apply filters
    filtered_df = df.copy()
    if filter_type != "All":
        filtered_df = filtered_df[filtered_df['type'] == filter_type]
    if filter_category != "All":
        filtered_df = filtered_df[filtered_df['category'] == filter_category]
    
    # Limit results
    if show_count != "All":
        filtered_df = filtered_df.head(show_count)
    
    # Display transactions
    if len(filtered_df) > 0:
        # Format the dataframe for display
        display_df = filtered_df.copy()
        display_df['amount'] = display_df.apply(
            lambda row: f"${row['amount']:,.2f}" if row['type'] == 'income' else f"-${row['amount']:,.2f}",
            axis=1
        )
        display_df['date'] = pd.to_datetime(display_df['date']).dt.strftime('%Y-%m-%d %H:%M')
        
        # Style the dataframe
        def color_type(val):
            if 'income' in str(val).lower():
                return 'color: #27ae60'
            elif 'expense' in str(val).lower():
                return 'color: #e74c3c'
            return ''
        
        styled_df = display_df.style.applymap(color_type, subset=['type'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)
        
        # Download button
        csv = df.to_csv(index=False)
        st.download_button(
            label="📥 Download data as CSV",
            data=csv,
            file_name=f"expenses_{datetime.now().strftime('%Y%m%d')}.csv",
            mime="text/csv"
        )
    else:
        st.info("No transactions match your filters")

if __name__ == "__main__":
    main()
