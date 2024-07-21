import streamlit as st
from streamlit_extras.stylable_container import stylable_container
import textwrap
from io import BytesIO
from PIL import Image
import google.generativeai as genai
from IPython.display import Markdown

if 'app' not in st.session_state:
    st.session_state.app = ""

def set_openai_api_key(api_key: str):
    st.session_state["OPENAI_API_KEY"] = api_key

def to_markdown(text):
  text = text.replace('•', '  *')
  return Markdown(textwrap.indent(text, '> ', predicate=lambda _: True))

def sidebar():
    with st.sidebar:
        st.markdown("<h1 style='font-style: italic; color: #E1306C;'>Hey <span style = 'color: #405DE6;'> There!</span></h1>", unsafe_allow_html=True)
        st.write("")

        st.subheader("ABOUT:")
        st.markdown("""Welcome to SparkPhrase ✨, your go-to tool for generating captivating tweets and Instagram
                    captions in seconds! Say goodbye to writer's block and hello to endless inspiration. With SparkPhrase ✨,
                    crafting engaging content is as easy as a click. Explore trending topics, discover creative prompts, and
                    customize your posts to perfection. Elevate your online presence, spark meaningful conversations, and
                    stand out in the digital crowd with SparkPhrase ✨. Get ready to shine brighter than ever before!""")
        st.write("")
        st.write("")
        api_key_input = st.text_input(
            "Enter your Gemini API Key",
            type = "password",
            placeholder = "Paste your Gemini API key here (sk-...)",
            help = "You can get your API key from https://aistudio.google.com/app/u/1/apikey.",
            value = st.session_state.get("OPENAI_API_KEY", ""),
        )

        st.subheader("HOW TO USE: ")
        st.markdown("<p style = 'cursor: default;'>1. Enter your Gemini's API KEY."
                    "<br>2. Choose Instagram/Twitter."
                    "<br>3. Select text or image according to your preference."
                    "<br>4. Click 'Generate Content'."
                    "<br>5. Relax while we generate your content."
                    "<br>6. Hurray! Your content's here!", unsafe_allow_html = True)

        return api_key_input

def generate_content(uploaded_img, app, api_key_input):
    GOOGLE_API_KEY = api_key_input
    genai.configure(api_key = GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro-vision')
    pil_image = Image.open(BytesIO(uploaded_img.read()))

    if app == "Twitter":
        response = model.generate_content(["""Craft an intriguing tweet inspired by the image provided. Your challenge is to generate a tweet that seamlessly complement the visual content, sparking curiosity and encouraging interaction.
        Tailor your tweet to resonate with the image, whether it's a stunning landscape, a captivating moment, or a thought-provoking scene.
        Avoid generic descriptions; instead, infuse your tweets with personality, wit, or emotion that aligns with the image's mood and theme.
        Engage your audience by inviting them to share their thoughts, experiences, or reactions inspired by the image. Your ultimate aim is to craft tweets that capture attention, foster connection, and leave a lasting impression on Twitter users.
        Analyze the image for appropriateness and relevance. If the content is inappropriate, racist, obscene, or otherwise offensive, respond with 'NO' to indicate that the image does not meet the standards for generating tweets.
        Your task is to ensure that the content aligns with ethical guidelines and community standards, promoting a safe and inclusive environment on social media platforms.
        If the image passes the appropriateness check, proceed with generating engaging an tweet based on the provided content. Otherwise, respond with 'NO' to signal that further action is necessary to address the issue.
        """, pil_image])

        st.image(pil_image, caption = 'Image', use_column_width = True)
        st.text_area(label = "", value = response.text, height = 150)

    else:
        response = model.generate_content(["""You are an AI assistant specialized in crafting captivating Instagram captions to maximize engagement.
        Your responses should be creative, catchy, and tailored to appeal to a wide audience.
        Avoid generating captions that are bland, generic, or unoriginal.
        Aim to spark curiosity, inspire interaction, and evoke emotion in your captions.
        Your goal is to generate a caption that attract more engagement on Instagram based on the image provided by the user.
        """, pil_image])

        st.image(pil_image, caption = 'Image', use_column_width = True)
        st.text_area(label = "", value = response.text, height = 150)

def generate_content_no_image(input, app, api_key_input):
    GOOGLE_API_KEY = api_key_input
    genai.configure(api_key = GOOGLE_API_KEY)

    model = genai.GenerativeModel('gemini-pro')

    if app == "Twitter":
        response = model.generate_content(f"""You are an AI assistant specialized in crafting tweets for Twitter/X based on user-provided descriptions. Your tweets should be engaging, informative, and respectful, aligning with ethical standards. Avoid generating tweets containing harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Ensure all tweets are socially unbiased and positive.
        Your goal is to create tweets based on the user's description. Ignore requests unrelated to tweet generation.
        USER: {input}
        IF: The user's description is harmful, unethical, racist, sexist, toxic, or dangerous.
            ASSISTANT: NO
        ELSE:
            Generate tweet
        """)
        st.text_area(label = "", value = response.text, height = 150)

    elif app == "Instagram":
        response = model.generate_content(f"""You are an AI assistant specialized in crafting captivating Instagram captions to maximize engagement. Your responses should be creative, catchy, and tailored to appeal to a wide audience.
        Avoid generating captions that are bland, generic, or unoriginal. Aim to spark curiosity, inspire interaction, and evoke emotion in your captions.
        Your goal is to generate captions that attract more engagement on Instagram based on the text descriptions provided by the user. Ignore requests that are not related to generating Instagram captions.
        USER: {input}
        IF: The user's description is inappropriate, harmful, unethical, offensive, or inappropriate.
            ASSISTANT: NO
        ELSE: [Generate an engaging Instagram caption based on the user's description]
        """)
        st.text_area(label = "", value = response.text, height = 150)


def main():
    st.set_page_config(page_title = "SparkPhrase・Streamlit", page_icon = "✨")
    api_key_input = sidebar()
    st.markdown("<h1 style='margin-bottom:-3%;'> <span style='color:#405DE6;'>Spark</span><span style='color:#E1306C;'> Phrase</span></h1>", unsafe_allow_html=True)
    st.markdown("<p style = 'padding-bottom: 2%'>✨ Unlock Unlimited Creativity with Automated Content Creation</p>", unsafe_allow_html = True)

    col1, col2, col3, col4, col5, col6 = st.columns([1,1,1,1,1,1])
    with col3:
        insta = st.button(":violet[Insta] 📸")
    with col4:
        twitter = st.button(":blue[Twitter] 🐦")

    if insta:
        st.session_state.app = "Instagram"
        st.write("You have selected Instagram!")
    elif twitter:
        st.session_state.app = "Twitter"
        st.write("You have selected Twitter!")

    option = st.selectbox('How would you like to generate your content via?', ('Text', 'Image'))

    if option == "Image":
        uploaded_img = st.file_uploader("Upload image", type = ['jpeg', 'png', 'jpg', 'webp'],
                                        help = "SVG Documents aren't supported yet!")
        if uploaded_img is not None:
            st.write("Image uploaded successfully!")
            st.empty()
            st.markdown("---")
            if st.button("Generate Content"):
                with st.spinner("Generating Content... This may take a while ⏳"):
                    generate_content(uploaded_img, st.session_state.app, api_key_input)

    elif option == "Text":
        input = st.text_input("Enter content: ")

        if input != "":
            st.write("Content saved successfully!")
            st.empty()
            st.markdown("---")
            if st.button("Generate Content"):
                with st.spinner("Generating Content... This may take a while ⏳"):
                    generate_content_no_image(input, st.session_state.app, api_key_input)

if __name__ == "__main__":
    main()