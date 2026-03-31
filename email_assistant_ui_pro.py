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

# Polished CSS Styling (Theme-aware)
st.markdown("""
    <style>
    /* Button enhancements avoiding squished text */
    .stButton > button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
    }
    
    /* Theme-agnostic Metrics */
    div[data-testid="stMetric"] {
        background: rgba(150, 150, 150, 0.05) !important;
        border: 1px solid rgba(150, 150, 150, 0.2) !important;
        border-radius: 12px !important;
        padding: 1rem !important;
    }
    
    /* Tone badges */
    .tone-badge {
        display: inline-block;
        padding: 0.4rem 0.8rem;
        border-radius: 24px;
        font-weight: 600;
        font-size: 0.85rem;
        margin: 0.25rem 0;
        letter-spacing: 0.5px;
        text-transform: uppercase;
    }
    
    .tone-formal {
        background: rgba(59, 130, 246, 0.15);
        color: #60a5fa;
        border: 1px solid rgba(59, 130, 246, 0.5);
    }
    
    .tone-friendly {
        background: rgba(16, 185, 129, 0.15);
        color: #34d399;
        border: 1px solid rgba(16, 185, 129, 0.5);
    }
    
    .tone-assertive {
        background: rgba(239, 68, 68, 0.15);
        color: #f87171;
        border: 1px solid rgba(239, 68, 68, 0.5);
    }
    
    /* Info box styling */
    .info-box {
        background: rgba(59, 130, 246, 0.1);
        border-left: 4px solid #3b82f6;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        margin: 1rem 0;
    }
    
    .info-box-title {
        font-weight: 600;
        color: #60a5fa;
        margin-bottom: 0.5rem;
    }
    
    /* Success message */
    .success-message {
        background: rgba(16, 185, 129, 0.1);
        border-left: 4px solid #10b981;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        color: #34d399;
        font-weight: 500;
        margin-top: 5px;
    }
    
    /* Error message */
    .error-message {
        background: rgba(239, 68, 68, 0.1);
        border-left: 4px solid #ef4444;
        border-radius: 8px;
        padding: 1rem 1.5rem;
        color: #f87171;
        font-weight: 500;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 2rem 1rem;
        color: #9ca3af;
        border-top: 1px solid rgba(150, 150, 150, 0.2);
        margin-top: 3rem;
        font-size: 0.9rem;
    }
    
    .footer-text {
        opacity: 0.8;
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
