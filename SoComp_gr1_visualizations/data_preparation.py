#!/usr/bin/env python
# coding: utf-8

# Import necessary files
import pandas as pd
from bokeh.models import ColumnDataSource, HoverTool
import bokeh.palettes as bp


# Description of parameters for axis labels
parameter_dict = {
    "vote_nr": "Vote number",
    "vote_title": "Official vote title",
    "topic_text": "Topics",
    "topic_main": "Main topic",
    "topic_sub": "Sub-topic",
    "voting_date": "Date of voting",
    "political_affiliation": "Political Affiliation that supported vote",
    "voter_turnout": "Voter turnout",
    "voting_result": "Result of Vote (in %)",
    "staendemehr": "Ständemehr",
    "verdict": "Verdict",
    "nof_ads_print": "Number of ads in printing medias",
    "yes_ads": "Percentage of YES ads",
    "nof_mediareport": "Number of Medienberichterstattungen",
    "tonality_mediareport": "Tonality in Medienberichterstattungen",
    "lz_timeperiod": "LZ Time period of relevance",
    "lz_nof_letters": "LZ Nof Reader's Letters",
    "lz_nof_writers": "LZ Nof writers",
    "lz_avg_letters_writer": "LZ Average letters/writer",
    "lz_avg_len_letter": "LZ Average length of letter (in words)",
    "lz_med_len_letter": "LZ Median length of letter (in words)",
    "lz_avg_opinion": "LZ Average Opinion",
    "20m_timeperiod": "20min Time period of relevance",
    "20m_nof_arcitles": "20min Number of Articles",
    "20m_nof_comments": "20min Number of Comments",
    "20m_avg_comments_article": "20min Average Comments (no/article)",
    "20m_nof_commentators": "20min Number of commentators",
    "20m_avg_comments_commentator": "20min Average Comments/commentators",
    "20m_avg_len_comment": "20min Average length of comment (in words)",
    "20m_med_len_comment": "20min Median length of comment (in words)",
    "20m_nof_comments_positive": "20min Number of comments positive",
    "20m_nof_comments_neutral": "20min Number of comments neutral",
    "20m_nof_comments_negative": "20min Number of comments negative",
    "20m_tendency_positive": "20min Tendency to positive comments",
    "20min_reactions_positive": "20min Number of reactions to positive comments",
    "20m_tendency_neutral": "20min Tendency to neutral comments",
    "20min_reactions_neutral": "20min Number of reactions to neutral comments",
    "20m_tendency_negative": "20min Tendency to negative comments",
    "20min_reactions_negative": "20min Number of reactions to negative comments"
}

def collect_and_wash():
    
    # Read data into a dataframe using pandas
    df = pd.read_csv('SoComp_clean_datasheet.csv')
    
    # ***********  Clean the data  *********** #
    
    # Convert "vote_nr" attribute to string
    df['vote_nr'] = "V" + df['vote_nr'].astype(str)
    
    # Assign collors to main topic
    topic_colors = bp.Set3[max(df['topic_main'])]
    df['topic_color'] = df['topic_main'].apply(lambda topic: topic_colors[topic - 1])
    
    # Convert "voting_date" to datetime type
    df['voting_date'] = pd.to_datetime(df['voting_date'], infer_datetime_format=True)
    
    # Assign collors and descriptions to political affiliation
    # Source: https://medium.com/srf-schweizer-radio-und-fernsehen/wie-wir-bei-srf-parteien-einfärben-9f010f80cf62
    pol_desc = ["Partei-übergreifend/parteilos", "Grüne, SP", "EVP", "Mitte, GLP", "FDP", "SVP"]
    pol_colors = ["#cccccc", "#ff0000", "#ff8700", "#beef00", "#063cff", "#009a2e"]
    df['pol_desc'] = df['political_affiliation'].apply(lambda aff: pol_desc[aff])
    df['pol_colors'] = df['political_affiliation'].apply(lambda aff: pol_colors[aff])
    
    # Convert "voter_turnout" attribute to float
    df['voter_turnout'] = df['voter_turnout'].str.rstrip('%').astype('float')
    
    # Convert "voting_result" attribute to float
    df['voting_result'] = df['voting_result'].str.rstrip('%').astype('float')
    df['voting_result_norm'] = df['voting_result']/100

    # Convert "staendemehr" attribute to float
    df['staendemehr'] = df['staendemehr'].str.rstrip('%').astype('float')
    
    # Convert "yes_ads" attribute to float
    df['yes_ads'] = df['yes_ads'].str.rstrip('%').astype('float')

    # Assign collors and markers to verdict
    verdict_colors = {"YES": "#2ca02c", "NO": "#d62728"}
    verdict_markers = {"YES": "star", "NO": "diamond"}
    df['verdict_color'] = df['verdict'].apply(lambda v: verdict_colors[v])
    df['verdict_markers'] = df['verdict'].apply(lambda v: verdict_markers[v])

    # ***********  Washing complete  *********** #
    
    # Convert dataframe to ColumnDataSource
    cds = ColumnDataSource(df)
    
    return cds
