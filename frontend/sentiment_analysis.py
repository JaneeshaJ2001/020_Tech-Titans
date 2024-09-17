import streamlit as st
from streamlit_option_menu import option_menu
from streamlit_elements import elements, mui, html, nivo
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import folium
import geopandas as gpd
from streamlit_folium import st_folium


def sentiment_analysis_page():
    
    sub_selected = option_menu(
        None,  # No title for sub-menu
        ["Analyze Social Media", "Public Opinion Trends", "Polling Details"],  # Sub-menu options
        icons=["info", "bar-chart", "twitter"],  # Sub-menu icons
        menu_icon="cast",  # Sub-menu menu icon
        default_index=0,  # Default selected sub-menu item
        orientation="horizontal",  # Make the sub-menu horizontal
        styles={
            
            "nav-link": {"font-size": "16px"},
            "nav-link-selected": {"background-color": "#b0e57c", "color": "black"},
        }
    )
    
    # Display content based on sub-menu selection
    if sub_selected == "Analyze Social Media":     
        
        st.title("Social Media Sentiment Analysis")

        st.markdown("""
                <style>
                .chart-container {
                    border: 2px solid gray;  /* Gray border */
                    padding: 10px;  /* Some padding around the chart */
                    border-radius: 10px;  /* Rounded corners */
                    box-shadow: 2px 2px 5px rgba(0,0,0,0.1);  /* Optional: A subtle shadow */
                    margin-bottom: 20px;  /* Space after the container */
                }
                </style>
            """, unsafe_allow_html=True)

        col1, col2, col3, col4 = st.columns(4)

        with col1:
                st.subheader("Anura Kumara Dissanayake")
                labels = ['Positive', 'Negative', 'Neutral']
                values = [50, 30, 20]  # These values should represent the percentage or count

                # Create the pie chart
                fig_target = go.Figure(data=[go.Pie(labels=labels,
                                                    values=values,
                                                    hole=.3)])

                fig_target.update_layout(
                    showlegend=True,
                    height=250,
                    margin={'l': 20, 'r': 60, 't': 0, 'b': 50},
                    legend=dict(
                        orientation="h",  # Horizontal orientation
                        yanchor="top",  # Aligns the legend at the top
                        y=-0.1,  # Moves the legend below the chart
                    )
                )
                fig_target.update_traces(textposition='inside', textinfo='percent')

                # Wrap the chart in a custom container
                #st.markdown("<div class='chart-container'>", unsafe_allow_html=True)
                st.plotly_chart(fig_target, use_container_width=True)
                st.markdown("</div>", unsafe_allow_html=True)                  
            

        with col2:
                
                st.write("Ranil Wickramasinghe")

        with col3:
                
                st.write("Sajith Premadasa")

        with col4:
                
                st.write("Namal Rajapakshe")

        # Row 2 - Another set of visual data or analysis in horizontal bar chart
        col5, col6 = st.columns(2)

        with col5:
            st.write("Comparison based on Comments")

            df = pd.DataFrame(
                [["Anura Kumara Dissanayake", 5.6, 7.8, 5], ["Ranil Wickramasinghe", 5.8, 7.2, 4.9], ["Namal Rajapakshe", 5.8, 7.2, 4.9], ["Sajith Premadasa", 5.8, 7.2, 4.9]],
                columns=["Candidate","Positive", "Negative", "Neutral"]
            )

            fig = px.bar(df, x="Candidate", y=["Positive", "Negative", "Neutral"], barmode='group', height=400)
            # st.dataframe(df) # if need to display dataframe
            st.plotly_chart(fig)

        with col6:
            st.write("Comparison based on Reactions")

            df = pd.DataFrame(
                [["Anura Kumara Dissanayake", 5.6, 7.8, 5], ["Ranil Wickramasinghe", 5.8, 7.2, 4.9], ["Namal Rajapakshe", 5.8, 7.2, 4.9], ["Sajith Premadasa", 5.8, 7.2, 4.9]],
                columns=["Candidate","Positive", "Negative", "Neutral"]
            )

            fig = px.bar(df, x="Candidate", y=["Positive", "Negative", "Neutral"], barmode='group', height=400)
            # st.dataframe(df) # if need to display dataframe
            st.plotly_chart(fig)

    elif sub_selected == "Public Opinion Trends":
        st.write("Public Opinion Trends")
    
    elif sub_selected == "Polling Details":

        disg = gpd.read_file('data/District_geo.json')
        disg = disg[['ADM2_PCODE', 'geometry']]
        df = pd.read_csv('data/district voting.csv')
        df.drop(columns=['geometry', 'admin2Name_si'], inplace=True)
        district = disg.merge(df, on="ADM2_PCODE")

        # Create styled text for tooltips
        district['styled_district'] = '<span style="background-color: #4EBCB3; color: white; padding: 5px;">District: </span><span style="float: right;">' + district['admin2Name_en'] + '</span>'
        district['styled_akd'] = '<span style="background-color: #D9539B; color: white; padding: 5px;">Anura Kumara Dissanayake: </span><span style="float: right;">' + district['akd-final%'].astype(str) + '%</span>'
        district['styled_sajith'] = '<span style="background-color: #57BC4E; color: white; padding: 5px;">Sajith Premadasa: </span><span style="float: right;">' + district['sajith-final%'].astype(str) + '%</span>'
        district['styled_ranil'] = '<span style="background-color: #BC9F4E; color: white; padding: 5px;">Ranil Wickramasinghe: </span><span style="float: right;">' + district['ranil-final%'].astype(str) + '%</span>'
        district['styled_namal'] = '<span style="background-color: #D95355; color: white; padding: 5px;">Namal Rajapakshe: </span><span style="float: right;">' + district['namal-final%'].astype(str) + '%</span>'
        district['styled_others'] = '<span style="background-color: #800080; color: white; padding: 5px;">Others: </span><span style="float: right;">' + district['others-final%'].astype(str) + '%</span>'

        # Define style and highlight functions
        style_function = lambda x: {'fillColor': '#ffffff', 'color':'#000000', 'fillOpacity': 0.1, 'weight': 0.1}
        highlight_function = lambda x: {'fillColor': '#000000', 'color':'#000000', 'fillOpacity': 0.50, 'weight': 0.1}

        # Initialize folium map
        m = folium.Map(location=[7.8731, 80.7718], zoom_start=7.4)

        # Add choropleth layer
        choropleth = folium.Choropleth(
            geo_data=district,
            name='choropleth',
            data=district,
            columns=['ADM2_PCODE', 'obtainedFinalVotesPercentage'],
            key_on='properties.ADM2_PCODE',
            fill_color='PuRd',
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name='Voting Percentage',
        ).add_to(m)

        # Add interactive GeoJson layer
        INT = folium.features.GeoJson(
            district,
            style_function=style_function,
            control=False,
            highlight_function=highlight_function,
            tooltip=folium.features.GeoJsonTooltip(
                fields=['styled_district', 'styled_akd', 'styled_sajith', 'styled_ranil', 'styled_namal', 'styled_others'],
                aliases=['', '', '', '', '', ''],
                sticky=True
            )
        )
        m.add_child(INT)
        m.keep_in_front(INT)
        folium.LayerControl().add_to(m)

        col1, col2 = st.columns(2)

        # Display map in Streamlit using streamlit_folium
        with col1:
            st_folium(m, width=550, height=580)
        
        with col2:

            # Add nice styled candidate voting percentages
            st.markdown("""
                <div style="text-align: center; font-family: Arial, sans-serif;">
                <h2 style="font-weight: bold;">ALL ISLAND FINAL RESULT</h2>
                <table style="width: 100%; border-collapse: collapse; font-family: Arial, sans-serif;padding:5px;">
                    <thead>
                        <tr>
                            <th colspan="2" style="border: 2px solid black; padding: 8px; background-color: white; font-weight: bold;">ALL ISLAND</th>
                        </tr>
                        <tr>
                            <th style="border: 2px solid black; padding: 8px; background-color: #f0f0f0; font-weight: bold;">CANDIDATE'S NAME</th>
                            <th style="border: 2px solid black; padding: 8px; background-color: #f0f0f0; font-weight: bold;">OBTAINED VOTES PERCENTAGE</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr>
                            <td style="border: 2px solid black; padding: 8px; background-color: #D9539B; color: white; font-weight: bold;">Anura Kumara Dissanayake</td>
                            <td style="border: 2px solid black; padding: 8px; background-color: #D9539B; color: white; text-align: right;">48.39%</td>
                        </tr>
                        <tr>
                            <td style="border: 2px solid black; padding: 8px; background-color: #57BC4E; color: white; font-weight: bold;">Sajith Premadasa</td>
                            <td style="border: 2px solid black; padding: 8px; background-color: #57BC4E; color: white; text-align: right;">31.57%</td>
                        </tr>
                        <tr>
                            <td style="border: 2px solid black; padding: 8px; background-color: #BC9F4E; color: white; font-weight: bold;">Ranil Wickremesinghe</td>
                            <td style="border: 2px solid black; padding: 8px; background-color: #BC9F4E; color: white; text-align: right;">12.91%</td>
                        </tr>
                        <tr>
                            <td style="border: 2px solid black; padding: 8px; background-color: #D95355; color: white; font-weight: bold;">Namal Rajapaksa</td>
                            <td style="border: 2px solid black; padding: 8px; background-color: #D95355; color: white; text-align: right;">2.02%</td>
                        </tr>
                        <tr>
                            <td style="border: 2px solid black; padding: 8px; background-color: yellow; font-weight: bold;">P. Ariyenathran</td>
                            <td style="border: 2px solid black; padding: 8px; background-color: yellow; text-align: right;">1.12%</td>
                        </tr>
                        <tr>
                            <td style="border: 2px solid black; padding: 8px; background-color: #800080; color: white; font-weight: bold;">Others</td>
                            <td style="border: 2px solid black; padding: 8px; background-color: #800080; color: white; text-align: right;">3.99%</td>
                        </tr>
                        <tr>
                            <td colspan="2" style="border: 2px solid black; padding: 8px; text-align: right; font-weight: bold;">Total Polled Percentage: 79.75%</td>
                        </tr>
                    </tbody>
                </table>
            </div>

                """, unsafe_allow_html=True)
