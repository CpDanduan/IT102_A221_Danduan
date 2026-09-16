import streamlit as st
import textwrap

import danduan_bank_analysis
import danduan_bank_auth
import danduan_bank_utils
import danduan_bank_transactions
from danduan_bank_service import BankService

# ============================================================
# BANK SERVICE
# ============================================================

bank_service = BankService()

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Danduan Bank",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# CUSTOM BANKING THEME
# ============================================================

st.html(textwrap.dedent(
    """
    <style>

    /* --------------------------------------------------------
       MAIN APPLICATION
    -------------------------------------------------------- */

    .stApp {
        background-color: #5a6a85;
    }

    .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }


    /* --------------------------------------------------------
       SIDEBAR
    -------------------------------------------------------- */

    section[data-testid="stSidebar"] {
        background: linear-gradient(
            180deg,
            #082b4c 0%,
            #0b416e 100%
        );
    }

    section[data-testid="stSidebar"] * {
        color: white;
    }

    section[data-testid="stSidebar"] .stRadio label {
        padding: 10px;
        border-radius: 8px;
    }

    section[data-testid="stSidebar"] .stRadio label:hover {
        background-color: rgba(255,255,255,0.10);
    }


    /* --------------------------------------------------------
       HEADINGS
    -------------------------------------------------------- */

    h1, h2, h3 {
        color: #12324a;
    }


    /* --------------------------------------------------------
       BUTTONS
    -------------------------------------------------------- */

    .stButton > button {
        width: 100%;
        min-height: 45px;

        border-radius: 10px;

        border: 1px solid #d5e1ea;

        font-weight: 600;

        transition: 0.2s;
    }

    .stButton > button:hover {
        border-color: #1677b8;

        transform: translateY(-1px);

        box-shadow: 0px 4px 10px rgba(0,0,0,0.08);
    }


    /* --------------------------------------------------------
       METRIC CARDS
    -------------------------------------------------------- */

    div[data-testid="stMetric"] {

        background-color: white;

        border: 1px solid #e1e9f0;

        border-radius: 14px;

        padding: 18px;

        box-shadow:
            0px 4px 12px
            rgba(0, 0, 0, 0.05);
    }

    div[data-testid="stMetricLabel"] {
        color: #647789 !important;
    }

    div[data-testid="stMetricValue"] {
        color: #12324a !important;
    }


    /* --------------------------------------------------------
       BANK CARD
    -------------------------------------------------------- */

    .bank-card {

        background-color: white;

        border: 1px solid #e1e9f0;

        border-radius: 16px;

        padding: 24px;

        margin-bottom: 20px;

        box-shadow:
            0px 4px 14px
            rgba(0, 0, 0, 0.05);
    }


    /* --------------------------------------------------------
       BALANCE CARD
    -------------------------------------------------------- */

    .balance-card {

        background: linear-gradient(
            135deg,
            #082f52,
            #126da1
        );

        color: white;

        border-radius: 18px;

        padding: 30px;

        margin-bottom: 24px;

        box-shadow:
            0px 8px 22px
            rgba(8, 59, 99, 0.20);
    }

    .balance-label {

        font-size: 0.85rem;

        color: rgba(255,255,255,0.75);

        letter-spacing: 1px;

        margin-bottom: 8px;
    }

    .balance-amount {

        font-size: 2.5rem;

        font-weight: 750;

        color: white;

        margin-bottom: 10px;
    }

    .balance-info {

        font-size: 0.9rem;

        color: rgba(255,255,255,0.85);
    }


    /* --------------------------------------------------------
       BRANDING
    -------------------------------------------------------- */

    .brand {

        display: flex;

        align-items: center;

        gap: 12px;

        margin-bottom: 5px;
    }

    .brand-icon {

        width: 46px;

        height: 46px;

        display: flex;

        align-items: center;

        justify-content: center;

        background-color:
            rgba(255,255,255,0.12);

        border-radius: 12px;

        font-size: 24px;
    }

    .brand-name {

        font-size: 1.25rem;

        font-weight: 750;

        letter-spacing: 1px;
    }


    /* --------------------------------------------------------
       WELCOME TEXT
    -------------------------------------------------------- */

    .welcome-text {

        color: #718394;

        font-size: 0.9rem;

        margin-bottom: 3px;
    }


    /* --------------------------------------------------------
       SECTION TITLES
    -------------------------------------------------------- */

    .section-title {

        font-size: 1.15rem;

        font-weight: 700;

        color: #12324a;

        margin-top: 25px;

        margin-bottom: 15px;
    }


    /* --------------------------------------------------------
       INFORMATION BOX
    -------------------------------------------------------- */

    .info-box {

        background-color: #edf6fb;

        border-left: 4px solid #1677b8;

        border-radius: 8px;

        padding: 14px;

        margin: 15px 0;

        color: #35576d;
    }


    /* --------------------------------------------------------
       AUTHENTICATION AREA
    -------------------------------------------------------- */

    .auth-container {

        max-width: 850px;

        margin: 30px auto;
    }

    .auth-header {

        text-align: center;

        margin-bottom: 30px;
    }

    .auth-icon {

        font-size: 50px;

        margin-bottom: 5px;
    }

    .auth-header h1 {

        margin-bottom: 5px;
    }

    .auth-header p {

        color: #718394;
    }


    /* --------------------------------------------------------
       FOOTER
    -------------------------------------------------------- */

    .bank-footer {

        text-align: center;

        color: #82909c;

        font-size: 0.8rem;

        margin-top: 40px;

        padding-top: 20px;

        border-top: 1px solid #e1e9f0;
    }

    </style>
    """),
)

# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "account" not in st.session_state:
    st.session_state.account = None

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def format_money(amount):
    return danduan_bank_utils.format_currency(amount)
def get_account_transactions(account_number):
    return [
        transaction
        for transaction
        in danduan_bank_transactions.get_transactions()

        if transaction.get("account_number")
        == account_number
    ]
def show_brand():
    st.html(textwrap.dedent(
        """
        <div class="brand">

            <div class="brand-icon">
                🏦
            </div>

            <div>

                <div class="brand-name">
                    DANDUAN BANK
                </div>

                <div
                    style="
                    font-size:0.75rem;
                    color:#a9c1d3;
                    "
                >
                    Digital Banking
                </div>

            </div>

        </div>
        """,
        ),
    )
def show_balance_card(account):
    st.html(textwrap.dedent(
        f"""
        <div class="balance-card">

            <div class="balance-label">
                AVAILABLE BALANCE
            </div>

            <div class="balance-amount">
                {format_money(account.balance)}
            </div>

            <div class="balance-info">

                {account.get_account_type()}

                &nbsp; • &nbsp;

                Account ending in
                {str(account.account_number)[-4:]}

            </div>

        </div>
        """,
        ),
    )

# ============================================================
# LOGIN / REGISTRATION
# ============================================================

if not st.session_state.logged_in:
    st.html(textwrap.dedent(
        """
        <div class="auth-container">
        """,
        ),
    )

    # --------------------------------------------------------
    # BANK BRAND
    # --------------------------------------------------------

    st.html(textwrap.dedent(
        """
        <div class="auth-header">

            <div class="auth-icon">
                🏦
            </div>

            <h1>
                DANDUAN BANK
            </h1>

            <p>
                Secure and simple digital banking
            </p>

        </div>
        """,
        ),
    )


    # --------------------------------------------------------
    # LOGIN / REGISTER TABS
    # --------------------------------------------------------

    login_tab, register_tab = st.tabs(
        [
            "🔐  Sign In",
            "➕  Open Account",
        ]
    )


    # ========================================================
    # LOGIN
    # ========================================================

    with login_tab:

        st.subheader("Welcome Back")

        st.caption(
            "Enter your account details to access your ATM."
        )


        account_number = st.text_input(
            "Account Number",
            key="login_account",
            placeholder="Enter your account number",
        )


        pin = st.text_input(
            "4-Digit PIN",
            type="password",
            max_chars=4,
            key="login_pin",
            placeholder="••••",
        )


        st.html(textwrap.dedent(
            """
            <div class="info-box">

                🔒 Your PIN is used only
                to verify your account.

            </div>
            """,
            ),
        )


        if st.button(
            "🔐  Sign In Securely",
            use_container_width=True,
        ):

            account, message = (
                danduan_bank_auth.login_account(
                    account_number,
                    pin,
                )
            )


            if account is not None:

                st.session_state.logged_in = True

                st.session_state.account = account

                st.success(message)

                st.rerun()

            else:

                st.error(message)


    # ========================================================
    # REGISTRATION
    # ========================================================

    with register_tab:

        st.subheader(
            "Create Your Danduan Bank Account"
        )

        st.caption(
            "Open your account in a few simple steps."
        )


        name = st.text_input(
            "Full Name",
            key="register_name",
            placeholder="Enter your full name",
        )


        account_number = st.text_input(
            "Account Number",
            key="register_account",
            placeholder="Choose an account number",
        )


        col1, col2 = st.columns(2)


        with col1:

            pin = st.text_input(
                "Create 4-Digit PIN",
                type="password",
                max_chars=4,
                key="register_pin",
                placeholder="••••",
            )


        with col2:

            confirm_pin = st.text_input(
                "Confirm PIN",
                type="password",
                max_chars=4,
                key="register_confirm_pin",
                placeholder="••••",
            )


        col1, col2 = st.columns(2)


        with col1:

            account_type = st.selectbox(
                "Account Type",
                [
                    "Savings Account",
                    "Student Account",
                ],
            )


        with col2:

            starting_balance = st.number_input(
                "Starting Balance",
                min_value=0.0,
                step=100.0,
                format="%.2f",
            )


        if st.button(
            "➕  Create Account",
            use_container_width=True,
        ):

            account, message = (
                danduan_bank_auth.register_account(
                    name,
                    account_number,
                    pin,
                    confirm_pin,
                    account_type,
                    starting_balance,
                )
            )


            if account is not None:

                st.success(message)

                st.info(
                    "Your account has been created. "
                    "Select the Sign In tab to continue."
                )

            else:

                st.error(message)


    st.html(textwrap.dedent(
        """
        <div class="bank-footer">

            🛡️ Danduan Bank
            • Secure Digital Banking
            • Personal ATM

        </div>
        """,
        ),
    )


# ============================================================
# LOGGED-IN ATM
# ============================================================

else:

    account = st.session_state.account


    transactions = get_account_transactions(
        account.account_number
    )


    # ========================================================
    # SIDEBAR
    # ========================================================

    with st.sidebar:

        show_brand()

        st.divider()


        st.html(textwrap.dedent(
            f"""
            **{account.account_name}**

            <span
                style="
                color:#b7cedf;
                font-size:0.8rem;
                "
            >
                <br>
                {account.get_account_type()}
                <br>
                {str(account.account_number)[-4:]}
            </span>
            """,
            ),
        )

        st.divider()
        st.caption("ATM SERVICES")

        menu = st.radio(
            "ATM SERVICES",
            [
                "🏠  Dashboard",
                "💵  Deposit",
                "💳  Withdraw",
                "🧾  Transaction History",
                "📊  Transaction Analysis",
            ],
            label_visibility="collapsed",
        )
        st.divider()
        if st.button(
            "↪  Logout",
            use_container_width=True,
        ):

            st.session_state.logged_in = False

            st.session_state.account = None

            st.rerun()


        st.html(textwrap.dedent(
            """
            <div
                style="
                margin-top:20px;
                font-size:0.75rem;
                color:#9fb8ca;
                "
            >

                🛡️ Secure Banking

                <br>

                Danduan Bank Digital ATM

            </div>
            """,
            ),
        )


    # ========================================================
    # REMOVE ICONS FROM MENU VALUE
    # ========================================================

    page = menu.split("  ", 1)[-1]


    # ========================================================
    # DASHBOARD
    # ========================================================

    if page == "Dashboard":

        st.html(textwrap.dedent(
            '<div class="welcome-text">PERSONAL ATM</div>',
            ),
        )

        st.title(
            f"Welcome, {account.account_name}"
        )


        show_balance_card(account)


        # ----------------------------------------------------
        # QUICK ACTIONS
        # ----------------------------------------------------

        st.html(textwrap.dedent(
            '<div class="section-title">Quick Actions</div>',
            ),
        )


        col1, col2, col3, col4 = st.columns(4)


        with col1:

            if st.button(
                "💵 Deposit",
                use_container_width=True,
            ):

                st.info(
                    "Select **Deposit** from "
                    "the ATM Services menu."
                )


        with col2:

            if st.button(
                "💳 Withdraw",
                use_container_width=True,
            ):

                st.info(
                    "Select **Withdraw** from "
                    "the ATM Services menu."
                )


        with col3:

            if st.button(
                "🧾 History",
                use_container_width=True,
            ):

                st.info(
                    "Select **Transaction History** "
                    "from the ATM Services menu."
                )


        with col4:

            if st.button(
                "📊 Analysis",
                use_container_width=True,
            ):

                st.info(
                    "Select **Transaction Analysis** "
                    "from the ATM Services menu."
                )


        # ----------------------------------------------------
        # ACCOUNT OVERVIEW
        # ----------------------------------------------------

        st.html(
            '<div class="section-title">Account Overview</div>',
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Current Balance",
            format_money(account.balance),
        )


        col2.metric(
            "Account Type",
            account.get_account_type(),
        )


        col3.metric(
            "Account Number",
            f"•••• {str(account.account_number)[-4:]}",
        )


        # ----------------------------------------------------
        # ACCOUNT INFORMATION
        # ----------------------------------------------------

        st.subheader(
            "🛡️ Account Information"
        )


        st.write(
            account.get_account_description()
        )


        st.html(
            """
            <div class="info-box">

                🔒 Your account is protected
                by PIN authentication.

                Use the ATM Services menu
                to manage your account.

            </div>
            """,
        )


        # ----------------------------------------------------
        # RECENT ACTIVITY
        # ----------------------------------------------------

        st.html(
            '<div class="section-title">Recent Activity</div>',
        )


        if transactions:

            recent_transactions = (
                transactions[-5:][::-1]
            )


            display_data = []


            for transaction in recent_transactions:

                display_data.append(
                    {
                        "Date & Time":
                            transaction.get(
                                "timestamp",
                                "N/A",
                            ),

                        "Transaction":
                            transaction.get(
                                "transaction",
                                "N/A",
                            ),

                        "Amount":
                            format_money(
                                transaction.get(
                                    "amount",
                                    0,
                                )
                            ),

                        "Balance":
                            format_money(
                                transaction.get(
                                    "balance_after",
                                    0,
                                )
                            ),
                    }
                )


            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True,
            )

        else:

            st.info(
                "No transactions yet. "
                "Your recent activity will appear here."
            )


    # ========================================================
    # DEPOSIT
    # ========================================================

    elif page == "Deposit":

        st.title("💵 Deposit Money")

        st.caption(
            "Add funds to your Danduan Bank account."
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Current Balance",
                format_money(account.balance),
            )


        with col2:

            amount = st.number_input(
                "Deposit Amount",
                min_value=0.0,
                step=100.0,
                format="%.2f",
            )


        st.html(
            """
            <div class="info-box">

                💡 Enter an amount greater than
                ₱0.00 to make a deposit.

            </div>
            """,
        )


        if st.button(
            "✓  Confirm Deposit",
            use_container_width=True,
        ):

            success, message = (
                bank_service.deposit(
                    account,
                    amount,
                )
            )


            if success:

                st.success(message)

                st.metric(
                    "New Balance",
                    format_money(account.balance),
                )

            else:

                st.error(message)


    # ========================================================
    # WITHDRAW
    # ========================================================

    elif page == "Withdraw":

        st.title("💳 Withdraw Money")

        st.caption(
            "Withdraw available funds from your account."
        )


        col1, col2 = st.columns(2)


        with col1:

            st.metric(
                "Available Balance",
                format_money(account.balance),
            )


        with col2:

            amount = st.number_input(
                "Withdrawal Amount",
                min_value=0.0,
                step=100.0,
                format="%.2f",
            )


        st.html(
            """
            <div class="info-box">

                💡 You can only withdraw an
                amount up to your available balance.

            </div>
            """,
        )


        if st.button(
            "✓  Confirm Withdrawal",
            use_container_width=True,
        ):

            success, message = (
                bank_service.withdraw(
                    account,
                    amount,
                )
            )


            if success:

                st.success(message)

                st.metric(
                    "New Balance",
                    format_money(account.balance),
                )

            else:

                st.error(message)


    # ========================================================
    # TRANSACTION HISTORY
    # ========================================================

    elif page == "Transaction History":

        st.title("🧾 Transaction History")

        st.caption(
            "Review your recent banking activity."
        )


        if transactions:

            deposits = sum(
                1
                for transaction in transactions
                if transaction.get("transaction")
                == "Deposit"
            )


            withdrawals = sum(
                1
                for transaction in transactions
                if transaction.get("transaction")
                == "Withdraw"
            )


            # ------------------------------------------------
            # SUMMARY
            # ------------------------------------------------

            col1, col2, col3 = st.columns(3)


            col1.metric(
                "Total Transactions",
                len(transactions),
            )


            col2.metric(
                "Deposits",
                deposits,
            )


            col3.metric(
                "Withdrawals",
                withdrawals,
            )


            st.html(
                '<div class="section-title">Activity</div>',
            )


            display_data = []


            for transaction in transactions[::-1]:

                display_data.append(
                    {
                        "Date & Time":
                            transaction.get(
                                "timestamp",
                                "N/A",
                            ),

                        "Transaction":
                            transaction.get(
                                "transaction",
                                "N/A",
                            ),

                        "Amount":
                            format_money(
                                transaction.get(
                                    "amount",
                                    0,
                                )
                            ),

                        "Balance After":
                            format_money(
                                transaction.get(
                                    "balance_after",
                                    0,
                                )
                            ),
                    }
                )


            st.dataframe(
                display_data,
                use_container_width=True,
                hide_index=True,
            )


        else:

            st.info(
                "No transaction history available yet."
            )


    # ========================================================
    # TRANSACTION ANALYSIS
    # ========================================================

    elif page == "Transaction Analysis":

        st.title("📊 Transaction Analysis")

        st.caption(
            "Understand your banking activity at a glance."
        )


        result = (
            danduan_bank_analysis
            .analyze_transactions(
                account.account_number
            )
        )


        # ----------------------------------------------------
        # TRANSACTION SUMMARY
        # ----------------------------------------------------

        st.html(
            '<div class="section-title">'
            'Transaction Summary'
            '</div>',
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Total Transactions",
            result["total_transactions"],
        )


        col2.metric(
            "Deposits",
            result["deposits"],
        )


        col3.metric(
            "Withdrawals",
            result["withdrawals"],
        )


        # ----------------------------------------------------
        # MONEY FLOW
        # ----------------------------------------------------

        st.html(
            '<div class="section-title">'
            'Money Flow'
            '</div>',
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Total Deposited",
            format_money(
                result["total_deposited"]
            ),
        )


        col2.metric(
            "Total Withdrawn",
            format_money(
                result["total_withdrawn"]
            ),
        )


        col3.metric(
            "Net Cash Flow",
            format_money(
                result["net_cash_flow"]
            ),
        )


        # ----------------------------------------------------
        # ACCOUNT ACTIVITY
        # ----------------------------------------------------

        st.html(
            '<div class="section-title">'
            'Account Activity'
            '</div>',
        )


        col1, col2, col3 = st.columns(3)


        col1.metric(
            "Largest Transaction",
            format_money(
                result["largest_transaction"]
            ),
        )


        col2.metric(
            "Average Transaction",
            format_money(
                result["average_transaction"]
            ),
        )


        col3.metric(
            "Latest Transaction",
            result["latest_transaction"],
        )


        # ----------------------------------------------------
        # LATEST ACTIVITY
        # ----------------------------------------------------

        st.html(
            f"""
            <div class="info-box">

                🕒 <strong>Latest Activity:</strong>
                {result["latest_timestamp"]}

            </div>
            """,
        )


# ============================================================
# END OF APPLICATION
# ============================================================

""" 
######### Learning Signature ######### 
Programmed by: Cristian Paul P Danduan
Date Submitted: September 15, 2026
 
Program Description: This program is about bank service.
Reflection: I learned how to improve an existing code.
 
AI Usage
[ ] No AI Assistance - Completed independently without AI.
[ ] AI as Support Tool - Used AI for explanations, syntax, or minor corrections.
[/] AI as Collaborative Partner - Used AI to design, structure, or co-create significant code.
"""