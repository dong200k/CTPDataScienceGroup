import streamlit as st
import streamlit.components.v1 as components
from PIL import Image

ctp_logo = Image.open("images/ctp icon.png")
st.set_page_config(
    page_icon=ctp_logo,
    layout="wide"
)

# Create a page header
st.header("Welcome to meeting our team members!")

# Create three columns
col1, col2, col3 = st.columns(3, gap="large")

btn_col1,btn_col2,btn_col3 = st.columns([1,1,1],gap="large")

with col1:
    # display a picture
    st.image('images/jerry.png')
    components.html(
        """
            <h3>Jiale (Jerry) Chen</h3>
                <div class="team-info">
                    <p>Data Science Fellow, Cohort8</p>
                </div>
                <p>
                City College of New York Applied Mathematics Class of 2023,
                Interested in Data Science and Finance.
                </p>
        """
        )


with col2:
    # display a picture
    st.image('images/Gene.jpeg')
    components.html(
        """
            <h3>Jiale (Jerry) Chen</h3>
                <div class="team-info">
                    <p>Data Science Fellow, Cohort8</p>
                </div>
                <p>
                    CUNY Queens College, Computer Science Major, expected to graducate in the end of 2022.
                    Interested in Front-End development, Machine Learning, and Data Science. 
                </p>
        """
        )


with col3:
    # display a picture
    st.image('images/dong.jpeg')
    components.html(
        """
            <h3>Jiale (Jerry) Chen</h3>
                <div class="team-info">
                    <p>Data Science Fellow, Cohort8</p>
                </div>
                  City College of New York Computer Science Class of 2022.
                </p>
        """
        )

with btn_col1:
    st.markdown("[![Title](https://img.icons8.com/fluency/48/null/linkedin.png)](https://www.linkedin.com/in/jiale-jerry-chen/)")
with btn_col2:
    st.markdown("[![Title](https://img.icons8.com/fluency/48/null/linkedin.png)](https://www.linkedin.com/in/chingkung310/)")
with btn_col3:
    st.markdown("[![Title](https://img.icons8.com/fluency/48/null/linkedin.png)](https://www.linkedin.com/in/dong-huang-chen/)")