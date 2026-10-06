import streamlit as st
from collections import defaultdict

from expense import Expense, load_expenses, save_expenses


# -------------------- PAGE CONFIG --------------------

st.set_page_config(
    page_title="Expense Tracker",
    page_icon="💰",
    layout="wide"
)


# -------------------- CUSTOM CSS --------------------

st.markdown("""
<style>

.hero {
    padding: 1.5rem 1.8rem;
    border-radius: 18px;
    background: linear-gradient(135deg, #111827, #1f2937);
    color: white;
    margin-bottom: 1.5rem;
}

.hero h1 {
    margin: 0;
    font-size: 2.2rem;
}

.hero p {
    margin: 0.4rem 0 0;
    color: #d1d5db;
}

.section-title {
    font-size: 1.35rem;
    font-weight: 700;
    margin: 1rem 0;
}

div[data-testid="stMetric"] {
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 14px;
    padding: 15px;
}

.expense-card {
    padding: 1rem;
    border: 1px solid rgba(128, 128, 128, 0.2);
    border-radius: 14px;
    margin-bottom: 0.7rem;
}

.category-pill {
    padding: 4px 10px;
    border-radius: 20px;
    background: rgba(99, 102, 241, 0.15);
    font-size: 0.85rem;
}

footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)


# -------------------- LOAD EXPENSES --------------------

if "expenses" not in st.session_state:
    st.session_state.expenses = load_expenses()

expenses = st.session_state.expenses


# -------------------- SIDEBAR --------------------

st.sidebar.title("💰 Expense Tracker")
st.sidebar.caption("Personal finance, simplified.")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Add Expense", "Expenses", "Analytics"]
)

st.sidebar.divider()
st.sidebar.caption("Built with Python + OOP + JSON + Streamlit")


# -------------------- HELPERS --------------------

def category_totals():
    totals = defaultdict(float)

    for expense in expenses:
        totals[expense.category] += expense.amount

    return dict(totals)


def delete_expense(index):
    expenses.pop(index)
    save_expenses(expenses)
    st.session_state.expenses = expenses


# -------------------- DASHBOARD --------------------

if page == "Dashboard":

    st.markdown("""
    <div class="hero">
        <h1>💰 Expense Tracker</h1>
        <p>
            Track your spending, understand your habits,
            and stay in control.
        </p>
    </div>
    """, unsafe_allow_html=True)

    total = sum(expense.amount for expense in expenses)
    count = len(expenses)
    categories = len(set(expense.category for expense in expenses))
    average = total / count if count else 0

    c1, c2, c3, c4 = st.columns(4)

    c1.metric(
        "Total Spending",
        f"₹{total:,.2f}"
    )

    c2.metric(
        "Transactions",
        count
    )

    c3.metric(
        "Categories",
        categories
    )

    c4.metric(
        "Average Expense",
        f"₹{average:,.2f}"
    )

    st.markdown(
        '<div class="section-title">Spending by Category</div>',
        unsafe_allow_html=True
    )

    totals = category_totals()

    if totals:

        chart_data = {
            "Category": list(totals.keys()),
            "Amount": list(totals.values())
        }

        st.bar_chart(
            chart_data,
            x="Category",
            y="Amount"
        )

    else:
        st.info(
            "No expenses yet. Add your first expense to see analytics."
        )

    st.markdown(
        '<div class="section-title">Recent Expenses</div>',
        unsafe_allow_html=True
    )

    if not expenses:

        st.info("Your expense list is empty.")

    else:

        for expense in expenses[-5:][::-1]:

            col1, col2, col3 = st.columns([3, 1, 1])

            col1.write(f"**{expense.name}**")
            col2.write(f"₹{expense.amount:,.2f}")
            col3.write(f"`{expense.category}`")


# -------------------- ADD EXPENSE --------------------

elif page == "Add Expense":

    st.title("➕ Add Expense")
    st.caption("Record a new transaction.")

    with st.form(
        "add_expense_form",
        clear_on_submit=True
    ):

        name = st.text_input(
            "Expense Name",
            placeholder="e.g. College canteen"
        )

        amount = st.number_input(
            "Amount (₹)",
            min_value=0.0,
            step=10.0
        )

        category = st.selectbox(
            "Category",
            [
                "Food",
                "Travel",
                "Shopping",
                "Education",
                "Entertainment",
                "Bills",
                "Health",
                "Other"
            ]
        )

        submitted = st.form_submit_button(
            "Add Expense",
            use_container_width=True
        )

        if submitted:

            if not name.strip():

                st.error(
                    "Please enter an expense name."
                )

            elif amount <= 0:

                st.error(
                    "Amount must be greater than ₹0."
                )

            else:

                expense = Expense(
                    name.strip(),
                    amount,
                    category
                )

                expenses.append(expense)

                save_expenses(expenses)

                st.success(
                    "Expense added successfully! 🎉"
                )

                st.rerun()


# -------------------- ALL EXPENSES --------------------

elif page == "Expenses":

    st.title("📋 All Expenses")

    if not expenses:

        st.info(
            "No expenses found. Add your first expense."
        )

    else:

        search = st.text_input(
            "🔎 Search",
            placeholder="Search by name or category..."
        ).strip().lower()

        filtered = [
            (index, expense)
            for index, expense in enumerate(expenses)
            if search in expense.name.lower()
            or search in expense.category.lower()
        ]

        st.caption(
            f"Showing {len(filtered)} of {len(expenses)} expenses"
        )

        for index, expense in filtered:

            with st.container(border=True):

                col1, col2, col3, col4 = st.columns(
                    [3, 2, 2, 1]
                )

                col1.write(
                    f"**{expense.name}**"
                )

                col2.write(
                    f"₹{expense.amount:,.2f}"
                )

                col3.write(
                    f"`{expense.category}`"
                )

                if col4.button(
                    "🗑️",
                    key=f"delete_{index}"
                ):

                    delete_expense(index)

                    st.success(
                        "Expense deleted."
                    )

                    st.rerun()


# -------------------- ANALYTICS --------------------

elif page == "Analytics":

    st.title("📊 Analytics")

    if not expenses:

        st.info(
            "Add some expenses to unlock analytics."
        )

    else:

        totals = category_totals()

        st.subheader(
            "Category Spending"
        )

        chart_data = {
            "Category": list(totals.keys()),
            "Amount": list(totals.values())
        }

        st.bar_chart(
            chart_data,
            x="Category",
            y="Amount"
        )

        st.subheader(
            "Category Summary"
        )

        sorted_totals = sorted(
            totals.items(),
            key=lambda x: x[1],
            reverse=True
        )

        total_amount = sum(totals.values())

        for category, amount in sorted_totals:

            percentage = (
                amount / total_amount * 100
            )

            col1, col2, col3 = st.columns(
                [2, 2, 1]
            )

            col1.write(
                f"**{category}**"
            )

            col2.progress(
                min(percentage / 100, 1.0)
            )

            col3.write(
                f"₹{amount:,.2f}"
            )

        st.divider()

        highest = max(
            expenses,
            key=lambda x: x.amount
        )

        st.subheader(
            "💡 Quick Insight"
        )

        st.info(
            f"Your biggest single expense is "
            f"**{highest.name}** at "
            f"**₹{highest.amount:,.2f}**."
        )