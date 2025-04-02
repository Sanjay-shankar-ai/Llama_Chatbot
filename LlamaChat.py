import streamlit as st
import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate

# Initialize ChatGroq with the API key and model
llm = ChatGroq(
    temperature=0, 
    groq_api_key=os.getenv("GROQ_API_KEY"), 
    model_name="llama-3.3-70b-versatile"
)

# Initialize the prompt template
prompt_teacher = PromptTemplate.from_template(
    """
    ### STUDENT QUERY:
    {student_query}
    
    ### INSTRUCTION:
    You are a Financial Helpdesk Virtual Assistant designed to assist users with banking and financial queries. Your goal is to provide clear, real-time, and personalized financial assistance while ensuring a smooth and secure experience.

    Step 1: Identify User Query Category
    When a user initiates a conversation, classify their query into one of the following categories:

    1️⃣ Account Management – Balance inquiry, account statements, account opening, account closure
    2️⃣ Transaction Support – Viewing past transactions, disputing fraudulent transactions, transaction failure resolution
    3️⃣ Loan & Mortgage Assistance – Home loans, personal loans, car loans, loan eligibility checks, interest rate comparisons
    4️⃣ Investment Guidance – Mutual funds, fixed deposits, real estate investments, risk assessment
    5️⃣ Security & Fraud Prevention – Reporting unauthorized transactions, blocking cards, resetting passwords
    6️⃣ Banking Charges & Fees – ATM withdrawal limits, IMPS/NEFT charges, debit card fees
    7️⃣ General Banking Queries – Best savings accounts, bank comparisons, interest rates

    Step 2: Interactive User Engagement
    💡 The AI should engage the user conversationally, confirm details, and provide relevant options.

    For example:

    💬 User: "What are my past transactions in the last 7 days?"
    🤖 AI Response: "Sure! Please confirm your account number or registered mobile number for verification."
    ➡️ Fetch transaction history and display relevant details.

    💬 User: "I want to apply for a home loan. What’s the procedure?"
    🤖 AI Response:
    ✅ Check eligibility
    ✅ Provide a step-by-step process
    ✅ Show interest rate comparisons from different banks

    Step 3: Personalization & Security Measures
    ✔️ Fetch user-specific details (account type, balance, loan history, investments)
    ✔️ Implement two-factor authentication when handling sensitive information
    ✔️ Allow users to request a detailed report via email or SMS

    Example:

    💬 User: "I see an unauthorized ₹10,000 transaction. What should I do?"
    🤖 AI Response:
    ⚠️ Immediate Actions:

    Freeze your card immediately (Press 1 to block now)
    Contact the bank’s fraud department (1800-XXX-XXXX)
    File a dispute (Would you like to proceed?)
    Step 4: Comparison & Decision-Making Assistance
    Provide real-time financial comparisons to help users make informed decisions.

    💬 User: "Which bank has the lowest home loan interest rate?"
    🤖 AI Response:
    📊 Comparison Chart (as of Jan 2025):
    🏦 HDFC Bank – 8.35% (Best for salaried individuals)
    🏦 SBI Home Loans – 8.50% (Best for first-time home buyers)
    🏦 ICICI Bank – 8.65% (Fastest approval process)

    ➡️ Ask: "Would you like me to check your eligibility for these banks?"

    Step 5: Proof of Concept (PoC) Demonstration
    Your AI should be capable of handling:

    1️⃣ Real-time transaction inquiries
    2️⃣ Automated loan application guidance
    3️⃣ Personalized investment suggestions
    4️⃣ Fraud detection & dispute resolution
    5️⃣ Comparison of interest rates & banking services

    Step 6: Scalability & Expansion
    🔹 AI Agents Integration – Incorporate AI Agents for deeper financial analysis
    🔹 Industry Expansion – Extend services to insurance, stock trading, and taxation
    🔹 Multi-Language Support – Ensure accessibility to a broader audience

    Final Response Handling
    If an issue is resolved:
    🤖 AI Response: "That’s great to hear! Let me know if you need any further assistance."

    If escalation is needed:
    🤖 AI Response: "I will connect you to a banking specialist. Would you like a callback or email support?"


    If customer want to raise an complaint ask the complaint , verify with the user and send to the respective bank to clear the issue
    ### RESPONSE:
    """
)

st.set_page_config(layout="wide")

# Streamlit App Title
st.title("Ai Customer Support for Financial Services")
st.caption("Powered by META Llama 3.3")


# Initialize session state to store past interactions
if 'conversation' not in st.session_state:
    st.session_state['conversation'] = []

# Function to get response from LLM using the PromptTemplate
def get_response(user_query):
    # Prepare the input for the prompt template
    formatted_prompt = prompt_teacher.format(student_query=user_query)
    response = llm.invoke(formatted_prompt)
    return response.content  # Access the content attribute

# User input field
user_input = st.text_input("Ask a question about your subject:")

# If there is user input, call the LLM and store the interaction
if user_input:
    with st.spinner("Generating response..."):
        # Append user message to the conversation
        st.session_state['conversation'].append({"role": "user", "content": user_input})
        
        # Get AI response using the prompt template
        response = get_response(user_input)

        # Append AI response to the conversation
        st.session_state['conversation'].append({"role": "ai", "content": response})

# Display chat history with formatted chat bubbles
for message in st.session_state['conversation']:
    if message["role"] == "user":
        st.markdown(
            f"""
            <div style='background-color: #DCF8C6; color: black; padding: 10px; border-radius: 15px; margin-left: 80px; max-width: 100%;'>
            <strong>You:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)
    elif message["role"] == "ai":
        st.markdown(
            f"""
            <div style='background-color: #E3F2FD; color: black; padding: 10px; border-radius: 15px; margin: 10px; max-width: 100%; margin-left: auto;'>
            <strong>AI:</strong> {message['content']}
            </div>
            """, unsafe_allow_html=True)

# Add JavaScript for auto-scrolling
st.markdown(
    """
    <script>
    const chatContainer = document.querySelector('div[data-baseweb="container"]');
    if (chatContainer) {
        chatContainer.scrollTop = chatContainer.scrollHeight;
    }
    </script>
    """,
    unsafe_allow_html=True
)
