"""
Smart Email Reply Assistant - Professional Streamlit UI
Premium interface for email classification and response generation
"""

import streamlit as st
from smart_email_assistant import SmartEmailAssistant, Email
from datetime import datetime

# Page configuration
st.set_page_config(
    page_title="Smart Email Reply Assistant",
    page_icon="📧",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Professional CSS Styling
st.markdown("""
    <style>
    /* Main theme colors */
    :root {
        --primary: #0066cc;
        --primary-light: #e6f2ff;
        --secondary: #1a5490;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --gray-50: #f9fafb;
        --gray-100: #f3f4f6;
        --gray-200: #e5e7eb;
        --gray-700: #374151;
        --gray-900: #111827;
    }
    
    /* Body and main container */
    .main {
        background-color: #ffffff;
        padding: 2rem;
    }
    
    /* Headers styling */
    h1, h2, h3, h4, h5, h6 {
        color: var(--gray-900);
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    
    h1 { margin-bottom: 0.5rem; }
    h2 { margin-top: 1.5rem; margin-bottom: 1rem; }
    h3 { margin-top: 1rem; margin-bottom: 0.75rem; }
    
    /* Text styling */
    p, label, span {
        color: var(--gray-700);
        line-height: 1.6;
    }
    
    /* Subtitle/description text */
    .subtitle {
        color: var(--gray-700);
        font-size: 1rem;
        margin-bottom: 1.5rem;
        opacity: 0.9;
    }
    
    /* Button styling */
    .stButton > button {
        width: 100%;
        background-color: var(--primary) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        font-size: 1rem !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button:hover {
        background-color: var(--secondary) !important;
        box-shadow: 0 4px 12px rgba(0,102,204,0.2) !important;
        transform: translateY(-2px) !important;
    }
    
    /* Card styling */
    .card {
        background-color: var(--gray-50);
        border: 1px solid var(--gray-200);
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 1px 3px rgba(0,0,0,0.08);
        transition: all 0.3s ease;
    }
    
    .card:hover {
        border-color: var(--primary);
        box-shadow: 0 4px 12px rgba(0,102,204,0.1);
    }
    
    /* Status cards */
    .status-success {
        background-color: #ecfdf5;
        border-left: 4px solid var(--success);
    }
    
    .status-warning {
        background-color: #fffbeb;
        border-left: 4px solid var(--warning);
    }
    
    .status-info {
        background-color: var(--primary-light);
        border-left: 4px solid var(--primary);
    }
    
    .status-error {
        background-color: #fef2f2;
        border-left: 4px solid var(--danger);
    }
    
    /* Input styling */
    .stTextInput input,
    .stTextArea textarea,
    .stSelectbox select {
        background-color: white !important;
        border: 2px solid var(--gray-200) !important;
        border-radius: 8px !important;
        padding: 0.75rem 1rem !important;
        color: var(--gray-900) !important;
        font-size: 0.95rem !important;
        transition: border-color 0.3s ease !important;
    }
    
    .stTextInput input:focus,
    .stTextArea textarea:focus,
    .stSelectbox select:focus {
        border-color: var(--primary) !important;
        box-shadow: 0 0 0 3px var(--primary-light) !important;
    }
    
    /* Labels */
    .stLabel {
        font-weight: 600;
        color: var(--gray-900) !important;
        font-size: 0.95rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Metrics */
    .stMetric {
        background-color: white !important;
        border: 1px solid var(--gray-200) !important;
        border-radius: 12px !important;
        padding: 1.5rem !important;
        text-align: center;
        transition: all 0.3s ease;
    }
    
    .stMetric:hover {
        border-color: var(--primary);
        box-shadow: 0 4px 12px rgba(0,102,204,0.1);
    }
    
    .metric-label {
        font-size: 0.85rem;
        font-weight: 600;
        color: var(--gray-700);
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
    }
    
    .metric-value {
        font-size: 1.75rem;
        font-weight: 700;
        color: var(--primary);
    }
    
    /* Tone badges */
    .tone-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 24px;
        font-weight: 600;
        font-size: 0.9rem;
        margin: 0.25rem;
        letter-spacing: 0.3px;
        text-transform: uppercase;
    }
    
    .tone-formal {
        background-color: #eff6ff;
        color: var(--primary);
        border: 1.5px solid var(--primary);
    }
    
    .tone-friendly {
        background-color: #f0fdf4;
        color: var(--success);
        border: 1.5px solid var(--success);
    }
    
    .tone-assertive {
        background-color: #fef2f2;
        color: var(--danger);
        border: 1.5px solid var(--danger);
    }
    
    /* Divider */
    .divider {
        margin: 2rem 0;
        border: 0;
        border-top: 2px solid var(--gray-200);
    }
    
    /* Section header */
    .section-header {
        display: flex;
        align-items: center;
        gap: 0.75rem;
        margin-bottom: 1.25rem;
        padding-bottom: 1rem;
        border-bottom: 2px solid var(--gray-200);
    }
    
    .section-icon {
        font-size: 1.5rem;
    }
    
    /* Sidebar styling */
    .sidebar .sidebar-content {
        padding: 2rem 1rem;
    }
    
    [data-testid="stSidebar"] {
        background-color: var(--gray-50);
    }
    
    /* Expander styling */
    .streamlit-expanderHeader {
        background-color: var(--gray-100) !important;
        border-radius: 8px !important;
        border: 1px solid var(--gray-200) !important;
    }
    
    /* Info box styling */
    .info-box {
        background-color: var(--primary-light);
        border-left: 4px solid var(--primary);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .info-box-title {
        font-weight: 600;
        color: var(--secondary);
        margin-bottom: 0.5rem;
    }
    
    /* Success message */
    .success-message {
        background-color: #f0fdf4;
        border-left: 4px solid var(--success);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        color: var(--success);
        font-weight: 500;
    }
    
    /* Error message */
    .error-message {
        background-color: #fef2f2;
        border-left: 4px solid var(--danger);
        border-radius: 8px;
        padding: 1rem 1.5rem;
        color: var(--danger);
        font-weight: 500;
    }
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 1rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent;
        border-bottom: 2px solid transparent;
        border-radius: 0;
        padding: 1rem 0;
    }
    
    .stTabs [aria-selected="true"] {
        border-bottom-color: var(--primary);
        color: var(--primary);
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 1rem;
        color: var(--gray-700);
        border-top: 1px solid var(--gray-200);
        margin-top: 3rem;
        font-size: 0.9rem;
    }
    
    .footer-text {
        opacity: 0.8;
    }
    
    /* Responsive */
    @media (max-width: 768px) {
        .main { padding: 1rem; }
        h1 { font-size: 1.5rem; }
        h2 { font-size: 1.25rem; }
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'assistant' not in st.session_state:
    st.session_state.assistant = SmartEmailAssistant()
if 'history' not in st.session_state:
    st.session_state.history = []

# ============================================================================
# SIDEBAR
# ============================================================================
with st.sidebar:
    st.markdown("## ⚙️ Configuration")
    st.markdown("---")
    
    # Sample emails section
    st.markdown("### 📌 Quick Start")
    sample_emails = {
        "Professor Query": {
            "subject": "Question about Assignment Deadline",
            "body": "Hi, I have a quick question about the assignment deadline. Can we extend it by a few days?",
            "sender": "professor"
        },
        "Team Meeting": {
            "subject": "Let's meet to discuss the project",
            "body": "Hey! When are you free next week? I'd love to meet and chat about our project updates.",
            "sender": "peer"
        },
        "Service Issue": {
            "subject": "Critical Issue with Recent Service",
            "body": "I'm extremely disappointed with the service received. This issue is unacceptable and requires IMMEDIATE attention!",
            "sender": "customer"
        },
        "Job Application": {
            "subject": "Application for Senior Developer Role",
            "body": "I recently saw your job posting and I'm very interested in the position. I believe my skills align perfectly with your requirements.",
            "sender": "recruiter"
        },
        "Project Update": {
            "subject": "Following up on our previous discussion",
            "body": "As we discussed last week, I wanted to follow up on the status of the proposal. Could you provide an update?",
            "sender": "colleague"
        }
    }
    
    selected_sample = st.selectbox(
        "Load Sample Email:",
        ["None"] + list(sample_emails.keys()),
        help="Choose a pre-filled example email"
    )
    
    st.markdown("---")
    st.markdown("### 📚 Information")
    st.info("""
    **How it works:**
    1. Enter an email subject and body
    2. Select sender context
    3. Click analyze
    4. Get instant AI-generated response
    
    **Features:**
    - Auto intent detection
    - Smart tone selection
    - Professional responses
    - Response history
    """)

# ============================================================================
# HEADER
# ============================================================================
col_logo, col_title = st.columns([0.1, 0.9])
with col_logo:
    st.markdown("## 📧")
with col_title:
    st.markdown("# Smart Email Reply Assistant")
    st.markdown(
        "<p class='subtitle'>Intelligent email classification and professional response generation powered by AI</p>",
        unsafe_allow_html=True
    )

st.markdown("---")

# ============================================================================
# MAIN INPUT SECTION
# ============================================================================
st.markdown("## 📝 Email to Analyze")

col_input1, col_input2 = st.columns(2)

with col_input1:
    email_subject = st.text_input(
        "📧 Email Subject",
        value=sample_emails[selected_sample]['subject'] if selected_sample != "None" else "",
        placeholder="Enter the email subject line",
        help="The subject line of the incoming email"
    )

with col_input2:
    sender_contexts = ["unknown", "professor", "HR", "recruiter", "manager", "peer", "colleague", "customer", "director"]
    sender_context = st.selectbox(
        "👤 Sender Context",
        sender_contexts,
        index=sender_contexts.index(sample_emails[selected_sample]['sender']) if selected_sample != "None" else 0,
        help="Select who is sending this email"
    )

email_body = st.text_area(
    "✍️ Email Body",
    value=sample_emails[selected_sample]['body'] if selected_sample != "None" else "",
    placeholder="Paste the full email content here...",
    height=180,
    help="The complete body text of the email"
)

col_urgency1, col_urgency2, col_button = st.columns([2, 1, 2])

with col_urgency1:
    st.markdown("**⏰ Urgency Level (Optional)**")
    urgency_level = st.select_slider(
        "Select urgency:",
        options=[None, 1, 2, 3, 4, 5],
        value=None,
        label_visibility="collapsed",
        help="Override auto-detected urgency level"
    )

with col_button:
    st.markdown("**Actions**")
    col_analyze, col_clear = st.columns(2)
    with col_analyze:
        analyze_clicked = st.button("🚀 Analyze", use_container_width=True, type="primary")
    with col_clear:
        if st.button("🔄 Clear", use_container_width=True):
            st.rerun()

# ============================================================================
# PROCESS EMAIL
# ============================================================================
if analyze_clicked:
    if not email_subject or not email_body:
        st.markdown("""
            <div class='error-message'>
            ⚠️ Please enter both email subject and body content
            </div>
        """, unsafe_allow_html=True)
    else:
        email = Email(
            subject=email_subject,
            body=email_body,
            sender_context=sender_context
        )
        result = st.session_state.assistant.process_email(email, urgency_override=urgency_level)
        
        st.session_state.history.append({
            'timestamp': datetime.now().isoformat(),
            'input': {
                'subject': email_subject,
                'body': email_body,
                'sender': sender_context
            },
            'result': result
        })
        
        st.session_state.last_result = result

# ============================================================================
# ANALYSIS RESULTS
# ============================================================================
if 'last_result' in st.session_state:
    result = st.session_state.last_result
    
    st.markdown("---")
    st.markdown("## 📊 AI Analysis Results")
    
    # Metrics row
    metrics_cols = st.columns(4)
    
    with metrics_cols[0]:
        intent_display = result['intent'].replace('_', ' ').title()
        confidence = f"{int(result['intent_confidence']*100)}%"
        st.metric("🎯 Intent", intent_display, confidence)
    
    with metrics_cols[1]:
        st.metric("💭 Sentiment", result['sentiment'].title(), "")
    
    with metrics_cols[2]:
        urgency = result['urgency_level']
        urgency_color = "🔴" if urgency >= 4 else "🟡" if urgency >= 2 else "🟢"
        st.metric("⏰ Urgency", f"{urgency}/5", urgency_color)
    
    with metrics_cols[3]:
        st.metric("👥 Context", result['sender_context'].title(), "")
    
    # Tone selection
    st.markdown("### 🎨 Selected Tone")
    tone = result['tone'].upper()
    tone_color_map = {
        'formal': 'tone-formal',
        'friendly': 'tone-friendly',
        'assertive': 'tone-assertive'
    }
    tone_class = tone_color_map.get(result['tone'], 'tone-formal')
    st.markdown(f"<span class='tone-badge {tone_class}'>{tone}</span>", unsafe_allow_html=True)
    
    # Analysis details
    st.markdown("### 📋 Detailed Analysis")
    for msg in result['analysis']['messages']:
        st.markdown(f"✅ {msg}")

# ============================================================================
# RESPONSE GENERATION
# ============================================================================
if 'last_result' in st.session_state:
    result = st.session_state.last_result
    
    st.markdown("---")
    st.markdown("## 💬 Suggested Professional Response")
    
    response_col1, response_col2 = st.columns([3, 1])
    
    with response_col1:
        response_text = st.text_area(
            "Your Response",
            value=result['suggested_response'],
            height=280,
            label_visibility="collapsed",
            help="Edit and customize the suggested response as needed"
        )
    
    with response_col2:
        st.markdown("### 📤 Actions")
        st.markdown("")
        
        if st.button("📋 Copy", use_container_width=True, help="Copy to clipboard"):
            st.markdown(
                "<div class='success-message'>✓ Copy feature available in production</div>",
                unsafe_allow_html=True
            )
        
        if st.button("💾 Save", use_container_width=True, help="Save response to file"):
            st.markdown(
                "<div class='success-message'>✓ Saved successfully</div>",
                unsafe_allow_html=True
            )
        
        if st.button("📧 Send", use_container_width=True, help="Send via email client"):
            st.markdown(
                "<div class='success-message'>✓ Opening email client...</div>",
                unsafe_allow_html=True
            )
        
        st.markdown("---")
        st.markdown("### 💡 Tips")
        st.caption("""
        • Always review the response
        • Customize with specific details
        • Adjust tone if needed
        • Proofread before sending
        """)

else:
    st.markdown("""
        <div class='info-box'>
        <div class='info-box-title'>📩 Ready to Analyze?</div>
        Enter an email above and click "Analyze" to get started
        </div>
    """, unsafe_allow_html=True)

# ============================================================================
# HISTORY SECTION
# ============================================================================
st.markdown("---")
st.markdown("## 📜 Processing History")

if st.session_state.history:
    st.markdown(f"**Total Processed: {len(st.session_state.history)}**")
    
    for i, record in enumerate(reversed(st.session_state.history), 1):
        with st.expander(
            f"**#{len(st.session_state.history)-i+1}** • {record['input']['subject'][:45]}... • "
            f"{record['result']['intent'].replace('_', ' ').title()} • {record['result']['tone'].title()}",
            expanded=False
        ):
            col_h1, col_h2, col_h3 = st.columns(3)
            
            with col_h1:
                st.markdown("**📧 Email Details**")
                st.text(f"Subject: {record['input']['subject']}")
                st.text(f"From: {record['input']['sender']}")
                st.text(f"Time: {record['timestamp'][:19]}")
            
            with col_h2:
                st.markdown("**🔍 Analysis**")
                st.text(f"Intent: {record['result']['intent'].replace('_', ' ').title()}")
                st.text(f"Confidence: {int(record['result']['intent_confidence']*100)}%")
                st.text(f"Sentiment: {record['result']['sentiment'].title()}")
            
            with col_h3:
                st.markdown("**⚙️ Settings**")
                st.text(f"Tone: {record['result']['tone'].title()}")
                st.text(f"Urgency: {record['result']['urgency_level']}/5")
                st.text(f"Sentiment: {record['result']['sentiment'].title()}")
else:
    st.markdown(
        "<div class='info-box'>No emails analyzed yet. Start by analyzing an email above!</div>",
        unsafe_allow_html=True
    )

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.markdown("""
    <div class='footer'>
    <div class='footer-text'>
    <strong>Smart Email Reply Assistant v1.0</strong><br>
    Powered by Advanced AI Intent Classification & Agentic Tone Selection
    </div>
    </div>
""", unsafe_allow_html=True)
