from collections import OrderedDict
import streamlit as st
from tabs import intro, Exploratory_data_analysis, pred_own_shot, conclusions, credits # , machine_learning_tab


st.set_page_config(
    page_title= "Analysis of NBA players' shots")

with open("style.css", "r") as f:
    style = f.read()

st.markdown(f"<style>{style}</style>", unsafe_allow_html=True)



# TODO: add new and/or renamed tab in this ordered dict by
# passing the name in the sidebar as key and the imported tab
# as value as follow :
TABS = OrderedDict(
    [
        (intro.sidebar_name, intro),
        (Exploratory_data_analysis.sidebar_name, Exploratory_data_analysis),
        # (machine_learning_tab.sidebar_name, machine_learning_tab),
        (pred_own_shot.sidebar_name, pred_own_shot),
        (conclusions.sidebar_name, conclusions),
        (credits.sidebar_name, credits),
    ]
)


def run():
      
    st.sidebar.image(
        "Ballon.png",
        width=250,
    )
    
                
    st.sidebar.markdown('<h1 style="color: #FFFFFF;">MENU</h1>', unsafe_allow_html=True)
    
    
    tab_name = st.sidebar.radio("", list(TABS.keys()), 0, key="tab_selector")

    

    
      
  
    tab = TABS[tab_name]
    
    
    tab.run()


if __name__ == "__main__":
    run()
