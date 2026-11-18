
import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase_client():

    url = st.secrets["SUPABASE_URL"].strip().rstrip("/")
    key = st.secrets["SUPABASE_KEY"].strip()

    return create_client(url, key)
