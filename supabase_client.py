
import streamlit as st
from supabase import create_client


@st.cache_resource
def get_supabase_client():
    """Create and reuse a Supabase connection."""

    supabase_url = st.secrets["SUPABASE_URL"]
    supabase_key = st.secrets["SUPABASE_KEY"]

    return create_client(
        supabase_url,
        supabase_key
    )
