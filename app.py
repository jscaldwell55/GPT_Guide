import streamlit as st
from openai import OpenAI

# Initialize OpenAI client using Streamlit secrets
client = OpenAI(
    api_key=st.secrets["OPENAI_API_KEY"])

# Page configuration
st.set_page_config(
    page_title="Randy's AI Learning Guide",
    page_icon="🤖",
    layout="wide"
)

# Define educational content
LEARNING_MODULES = {
    "Understanding LLMs": {
        "content": """
        Hey Randy! Let's start with the basics of Large Language Models (LLMs):
        
        - They're AI systems trained on massive amounts of text
        - They can understand and generate human-like text
        - They learn patterns from training data
        - They can help with writing, analysis, and problem-solving
        
        Think of them as incredibly well-read assistants who can help you think through problems and draft content.
        """,
        "example": "Explain artificial intelligence to someone new to the field",
        "tips": "Start with simple queries and notice how the AI structures its responses"
    },
    "Effective Prompting": {
        "content": """
        The key to getting good results is how you ask questions:
        
        - Be specific about what you want
        - Provide context when needed
        - Break complex requests into steps
        - Ask for examples or explanations
        - Request specific formats when needed
        
        The more clear and specific you are, the better the results!
        """,
        "example": "Write a clear explanation of inventory management, include three specific examples, and format it with bullet points",
        "tips": "Notice how adding specific requirements improves the response"
    },
    "Real-World Applications": {
        "content": """
        LLMs can help with many practical tasks:
        
        - Writing and editing documents
        - Analyzing data and trends
        - Explaining complex topics
        - Brainstorming ideas
        - Creating presentations
        - Learning new concepts
        
        Let's experiment with different types of tasks to see what works best for you.
        """,
        "example": "Help me understand machine learning algorithms and their practical applications",
        "tips": "Try both simple and complex queries to understand the AI's capabilities"
    }
}

def generate_response(prompt, include_explanation=True):
    """Generate response with optional explanation of AI thinking"""
    try:
        # Generate main response
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an educational AI assistant helping Randy learn about LLMs. Provide clear, informative responses that help him understand both the content and how AI thinks about questions."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7
        )
        
        if include_explanation:
            explanation = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "Explain how the AI approached this response and what Randy can learn from it about how LLMs work."},
                    {"role": "user", "content": f"Explain how this response demonstrates AI capabilities: {response.choices[0].message.content}"}
                ],
                temperature=0.7
            )
            return {
                "response": response.choices[0].message.content,
                "explanation": explanation.choices[0].message.content
            }
        
        return {"response": response.choices[0].message.content}
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None

# Main UI
st.title("🤖 Welcome to AI Learning, Randy!")
st.write("Let's explore the world of Large Language Models together")

# Sidebar with learning modules
with st.sidebar:
    st.header("Learning Journey")
    selected_module = st.selectbox("Choose a topic", list(LEARNING_MODULES.keys()))
    
    st.markdown("### About This Topic")
    st.markdown(LEARNING_MODULES[selected_module]["content"])
    
    st.markdown("### Try This Example")
    st.code(LEARNING_MODULES[selected_module]["example"])
    
    st.markdown("### Learning Tip")
    st.info(LEARNING_MODULES[selected_module]["tips"])

# Main content area
tab1, tab2 = st.tabs(["Try It Out", "Learning Resources"])

with tab1:
    st.header("Experiment with AI")
    with st.form("chat_form"):
        user_prompt = st.text_area(
            "What would you like to try?",
            placeholder="Type any question or task you'd like to explore...",
            height=100
        )
        
        col1, col2 = st.columns(2)
        with col1:
            show_explanation = st.checkbox("Show me how the AI thinks", value=True)
        
        submitted = st.form_submit_button("Let's see what happens")

    if submitted and user_prompt:
        with st.spinner("Thinking..."):
            result = generate_response(user_prompt, show_explanation)
            if result:
                st.markdown("### AI Response:")
                st.write(result["response"])
                
                if show_explanation:
                    with st.expander("Understanding the AI's Approach"):
                        st.markdown("### How the AI Thought About This:")
                        st.write(result["explanation"])

with tab2:
    st.header("Learning Resources")
    st.markdown("""
    ### Key Concepts
    - **Large Language Models (LLMs)**: AI systems trained on vast amounts of text data
    - **Prompting**: The art of effectively communicating with AI
    - **Context**: Helping the AI understand exactly what you need
    - **Capabilities**: Understanding what AI can and cannot do
    
    ### Tips for Better Results
    1. **Start Simple**: Begin with basic queries and gradually increase complexity
    2. **Be Specific**: Clear, detailed requests get better responses
    3. **Experiment**: Try different approaches to see what works best
    4. **Learn from Explanations**: Pay attention to how the AI thinks about your questions
    
    ### Common Applications
    - Writing and editing
    - Explaining complex topics
    - Analyzing information
    - Brainstorming ideas
    - Learning new concepts
    - Problem-solving
    """)

# Educational footer
with st.expander("💡 Quick Guide to AI Interaction"):
    st.markdown("""
    ### Getting Started
    - Start with simple questions to understand basic capabilities
    - Gradually try more complex tasks
    - Pay attention to how different types of prompts get different results
    
    ### Making the Most of AI
    - Use clear, specific language
    - Break complex tasks into smaller parts
    - Ask for explanations when needed
    - Experiment with different approaches
    
    ### Remember
    - AI is a tool to enhance thinking, not replace it
    - Responses should always be verified
    - The quality of output depends on the quality of input
    - Learning to use AI effectively takes practice
    """)