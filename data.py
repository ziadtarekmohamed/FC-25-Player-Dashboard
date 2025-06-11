import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

st.set_page_config(
    page_title="FC 25 Player Analytics Dashboard",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background: linear-gradient(90deg, #1e3c72, #2a5298);
        color: white;
        border-radius: 10px;
        margin-bottom: 2rem;
    }
    .metric-card {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        text-align: center;
    }
    .stSelectbox > div > div {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    try:
        df = pd.read_csv(r"WRITE_THE_PATH_OF_THE_DATASET")
        df = df.dropna(subset=['Name', 'OVR'])
        
        numeric_cols = ['Age', 'OVR', 'PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 
                       'Height', 'Weight', 'Weak foot', 'Skill moves']
        for col in numeric_cols:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce')
        
        df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
        
        return df
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return pd.DataFrame()

df = load_data()
if df.empty:
    st.stop()


st.markdown("""
<div class="main-header">
    <h1>⚽ FC 25 Player Analytics Dashboard</h1>
    <p>Comprehensive analysis of FIFA 25 player database</p>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("## 🔍 **Filters & Search**")

search_name = st.sidebar.text_input("🔎 Search Player by Name", placeholder="Enter player name...")
if search_name:
    df = df[df['Name'].str.contains(search_name, case=False, na=False)]

positions = ['All'] + sorted([pos for pos in df['Position'].dropna().unique() if pos != ''])
position = st.sidebar.selectbox("⚽ Position", positions)

nations = ['All'] + sorted([nation for nation in df['Nation'].dropna().unique() if nation != ''])
nation = st.sidebar.selectbox("🌍 Nation", nations)

teams = ['All'] + sorted([team for team in df['Team'].dropna().unique() if team != ''])
team = st.sidebar.selectbox("🏆 Team", teams)

if 'Age' in df.columns and not df['Age'].isna().all():
    age_min, age_max = int(df['Age'].min()), int(df['Age'].max())
    age_range = st.sidebar.slider("👤 Age Range", age_min, age_max, (age_min, age_max))
    filtered_df = df[(df['Age'] >= age_range[0]) & (df['Age'] <= age_range[1])]
else:
    filtered_df = df.copy()

ovr_min, ovr_max = int(df['OVR'].min()), int(df['OVR'].max())
ovr_range = st.sidebar.slider("⭐ Overall Rating Range", ovr_min, ovr_max, (ovr_min, ovr_max))

if position != 'All':
    filtered_df = filtered_df[filtered_df['Position'] == position]
if nation != 'All':
    filtered_df = filtered_df[filtered_df['Nation'] == nation]
if team != 'All':
    filtered_df = filtered_df[filtered_df['Team'] == team]

filtered_df = filtered_df[(filtered_df['OVR'] >= ovr_range[0]) & (filtered_df['OVR'] <= ovr_range[1])]

st.sidebar.markdown(f"**Results:** {len(filtered_df)} players found")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 **Overview**", 
    "⚔️ **Player Comparison**", 
    "🧤 **Goalkeepers**", 
    "📈 **Analytics**", 
    "🔍 **Player Search**"
])

with tab1:
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Players", len(filtered_df))
    with col2:
        st.metric("Avg Overall", f"{filtered_df['OVR'].mean():.1f}")
    with col3:
        st.metric("Teams", filtered_df['Team'].nunique())
    with col4:
        st.metric("Nations", filtered_df['Nation'].nunique())
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🏆 Top 15 Players by Overall Rating")
        top_players = filtered_df.nlargest(15, 'OVR')
        fig_top = px.bar(
            top_players, 
            x='OVR', 
            y='Name', 
            color='Position',
            orientation='h',
            title="Top Players by OVR",
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig_top.update_layout(height=600, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top, use_container_width=True)
    
    with col2:
        st.subheader("⚽ Position Distribution")
        pos_counts = filtered_df['Position'].value_counts().head(10)
        fig_pos = px.pie(
            values=pos_counts.values,
            names=pos_counts.index,
            title="Player Distribution by Position"
        )
        fig_pos.update_layout(height=400)
        st.plotly_chart(fig_pos, use_container_width=True)
        
        st.subheader("🌍 Top Nations")
        nation_counts = filtered_df['Nation'].value_counts().head(10)
        fig_nation = px.bar(
            x=nation_counts.values,
            y=nation_counts.index,
            orientation='h',
            title="Players by Nation (Top 10)"
        )
        fig_nation.update_layout(height=300, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_nation, use_container_width=True)
    
    st.subheader("📊 Attribute Analysis")
    attr_cols = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
    available_attrs = [col for col in attr_cols if col in filtered_df.columns]
    
    if available_attrs:
        selected_attr = st.selectbox("Choose Attribute to Analyze", available_attrs)
        
        col1, col2 = st.columns(2)
        with col1:
            top_attr = filtered_df.nlargest(10, selected_attr)
            fig_attr = px.bar(
                top_attr, 
                x=selected_attr, 
                y='Name', 
                color='Team',
                orientation='h',
                title=f'Top 10 Players by {selected_attr}'
            )
            fig_attr.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
            st.plotly_chart(fig_attr, use_container_width=True)
        
        with col2:
            fig_hist = px.histogram(
                filtered_df, 
                x=selected_attr, 
                nbins=20,
                title=f'{selected_attr} Distribution'
            )
            fig_hist.update_layout(height=400)
            st.plotly_chart(fig_hist, use_container_width=True)

with tab2:
    st.header("⚔️ Compare Players Head-to-Head")
    
    col1, col2 = st.columns(2)
    with col1:
        player1 = st.selectbox("🥇 Select Player 1", options=sorted(df['Name'].unique()), key="p1")
    with col2:
        player2 = st.selectbox("🥈 Select Player 2", options=sorted(df['Name'].unique()), key="p2")
    
    if player1 and player2 and player1 != player2:
        p1_data = df[df['Name'] == player1].iloc[0]
        p2_data = df[df['Name'] == player2].iloc[0]
        
        col1, col2 = st.columns(2)
        with col1:
            st.subheader(f"👤 {player1}")
            st.write(f"**Position:** {p1_data.get('Position', 'N/A')}")
            st.write(f"**Team:** {p1_data.get('Team', 'N/A')}")
            st.write(f"**Nation:** {p1_data.get('Nation', 'N/A')}")
            st.write(f"**Age:** {p1_data.get('Age', 'N/A')}")
            st.write(f"**Overall:** {p1_data.get('OVR', 'N/A')}")
        
        with col2:
            st.subheader(f"👤 {player2}")
            st.write(f"**Position:** {p2_data.get('Position', 'N/A')}")
            st.write(f"**Team:** {p2_data.get('Team', 'N/A')}")
            st.write(f"**Nation:** {p2_data.get('Nation', 'N/A')}")
            st.write(f"**Age:** {p2_data.get('Age', 'N/A')}")
            st.write(f"**Overall:** {p2_data.get('OVR', 'N/A')}")
        
        stats_cols = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
        available_stats = [col for col in stats_cols if col in df.columns]
        
        if available_stats:
            fig = go.Figure()
            
            fig.add_trace(go.Scatterpolar(
                r=[p1_data.get(stat, 0) for stat in available_stats],
                theta=available_stats,
                fill='toself',
                name=player1,
                line_color='blue'
            ))
            
            fig.add_trace(go.Scatterpolar(
                r=[p2_data.get(stat, 0) for stat in available_stats],
                theta=available_stats,
                fill='toself',
                name=player2,
                line_color='red'
            ))
            
            fig.update_layout(
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 100]
                    )),
                showlegend=True,
                title="Player Attributes Comparison",
                height=500
            )
            st.plotly_chart(fig, use_container_width=True)
            
            comparison_data = pd.DataFrame({
                'Attribute': available_stats,
                player1: [p1_data.get(stat, 0) for stat in available_stats],
                player2: [p2_data.get(stat, 0) for stat in available_stats]
            })
            
            fig_bar = px.bar(
                comparison_data.melt(id_vars='Attribute', var_name='Player', value_name='Rating'),
                x='Attribute',
                y='Rating',
                color='Player',
                barmode='group',
                title="Detailed Attribute Comparison"
            )
            st.plotly_chart(fig_bar, use_container_width=True)

with tab3:
    st.header("🧤 Goalkeeper Analysis")
    
    gk_cols = ['GK Diving', 'GK Handling', 'GK Kicking', 'GK Positioning', 'GK Reflexes']
    available_gk_cols = [col for col in gk_cols if col in df.columns]
    
    if available_gk_cols:
        gk_df = df[df[available_gk_cols].notnull().any(axis=1)].copy()
        
        if not gk_df.empty:
            col1, col2 = st.columns(2)
            
            with col1:
                st.subheader("🏆 Top 10 Goalkeepers by Reflexes")
                if 'GK Reflexes' in gk_df.columns:
                    top_gk = gk_df.nlargest(10, 'GK Reflexes')
                    fig_gk = px.bar(
                        top_gk,
                        x='GK Reflexes',
                        y='Name',
                        color='Team',
                        orientation='h',
                        title="Top Goalkeepers by Reflexes"
                    )
                    fig_gk.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
                    st.plotly_chart(fig_gk, use_container_width=True)
            
            with col2:
                st.subheader("📊 GK Attribute Analysis")
                selected_gk_attr = st.selectbox("Choose GK Attribute", available_gk_cols)
                
                if selected_gk_attr in gk_df.columns:
                    fig_hist_gk = px.histogram(
                        gk_df,
                        x=selected_gk_attr,
                        nbins=15,
                        title=f'{selected_gk_attr} Distribution'
                    )
                    st.plotly_chart(fig_hist_gk, use_container_width=True)
            
            st.subheader("🗂️ Detailed Goalkeeper Stats")
            display_cols = ['Name', 'Team', 'Nation', 'Age', 'OVR'] + available_gk_cols
            available_display_cols = [col for col in display_cols if col in gk_df.columns]
            
            gk_display = gk_df[available_display_cols].sort_values('OVR', ascending=False)
            st.dataframe(gk_display, use_container_width=True, height=400)
    else:
        st.warning("Goalkeeper-specific columns not found in the dataset.")

with tab4:
    st.header("📈 Advanced Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Age vs Overall Rating")
        if 'Age' in filtered_df.columns:
            fig_age = px.scatter(
                filtered_df,
                x='Age',
                y='OVR',
                color='Position',
                size='OVR',
                hover_data=['Name', 'Team'],
                title="Age vs Overall Rating Distribution"
            )
            st.plotly_chart(fig_age, use_container_width=True)
    
    with col2:
        st.subheader("🎯 Attribute Correlation")
        attr_cols = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY', 'OVR']
        available_attrs = [col for col in attr_cols if col in filtered_df.columns]
        
        if len(available_attrs) > 1:
            corr_matrix = filtered_df[available_attrs].corr()
            fig_corr = px.imshow(
                corr_matrix,
                title="Attribute Correlation Matrix",
                color_continuous_scale='RdBu'
            )
            st.plotly_chart(fig_corr, use_container_width=True)
    
    st.subheader("🏆 Team Analysis")
    col1, col2 = st.columns(2)
    
    with col1:
        team_stats = filtered_df.groupby('Team').agg({
            'OVR': ['mean', 'count'],
            'Age': 'mean'
        }).round(2)
        team_stats.columns = ['Avg_OVR', 'Player_Count', 'Avg_Age']
        team_stats = team_stats.reset_index()
        
        fig_team = px.scatter(
            team_stats,
            x='Avg_Age',
            y='Avg_OVR',
            size='Player_Count',
            hover_data=['Team'],
            title="Team Performance: Average Age vs Overall Rating"
        )
        st.plotly_chart(fig_team, use_container_width=True)
    
    with col2:
        st.subheader("🌟 Top Teams by Average Rating")
        top_teams = team_stats.nlargest(10, 'Avg_OVR')
        fig_top_teams = px.bar(
            top_teams,
            x='Avg_OVR',
            y='Team',
            orientation='h',
            title="Top 10 Teams by Average Overall Rating"
        )
        fig_top_teams.update_layout(height=400, yaxis={'categoryorder':'total ascending'})
        st.plotly_chart(fig_top_teams, use_container_width=True)

# Tab 5: Player Search
with tab5:
    st.header("🔍 Advanced Player Search & Details")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        min_ovr = st.number_input("Minimum Overall Rating", min_value=0, max_value=100, value=70)
    with col2:
        max_age = st.number_input("Maximum Age", min_value=15, max_value=50, value=35)
    with col3:
        min_players = st.number_input("Minimum results to show", min_value=1, max_value=100, value=20)
    
    search_df = filtered_df[
        (filtered_df['OVR'] >= min_ovr) & 
        (filtered_df['Age'] <= max_age)
    ].head(min_players)
    
    if not search_df.empty:
        selected_player = st.selectbox("Select a player for detailed view", search_df['Name'].unique())
        
        if selected_player:
            player_data = search_df[search_df['Name'] == selected_player].iloc[0]
            
            col1, col2 = st.columns([1, 2])
            
            with col1:
                st.subheader(f"👤 {selected_player}")
                info_cols = ['Position', 'Team', 'Nation', 'Age', 'OVR']
                for col in info_cols:
                    if col in player_data:
                        st.write(f"**{col}:** {player_data[col]}")
            
            with col2:
                attr_cols = ['PAC', 'SHO', 'PAS', 'DRI', 'DEF', 'PHY']
                available_attrs = [col for col in attr_cols if col in player_data.index]
                
                if available_attrs:
                    attr_values = [player_data.get(attr, 0) for attr in available_attrs]
                    
                    fig_player = go.Figure(go.Scatterpolar(
                        r=attr_values,
                        theta=available_attrs,
                        fill='toself',
                        name=selected_player
                    ))
                    
                    fig_player.update_layout(
                        polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
                        showlegend=True,
                        title=f"{selected_player} - Attribute Profile"
                    )
                    st.plotly_chart(fig_player, use_container_width=True)
        
        st.subheader("🗂️ Search Results")
        all_columns = search_df.columns.tolist()
        default_cols = ['Name', 'Position', 'Team', 'Nation', 'Age', 'OVR']
        display_columns = st.multiselect(
            "Select columns to display",
            all_columns,
            default=[col for col in default_cols if col in all_columns]
        )
        
        if display_columns:
            st.dataframe(search_df[display_columns], use_container_width=True, height=400)
        
        csv = search_df.to_csv(index=False)
        st.download_button(
            label="📥 Download Search Results",
            data=csv,
            file_name=f"fc25_search_results_{len(search_df)}_players.csv",
            mime="text/csv"
        )
    else:
        st.warning("No players found matching your criteria. Try adjusting the filters.")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>FC 25 Player Analytics Dashboard | Data insights for football enthusiasts ⚽</p>
</div>
""", unsafe_allow_html=True)
