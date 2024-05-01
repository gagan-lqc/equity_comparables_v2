from sentence_transformers import SentenceTransformer, util
import pandas as pd

def find_similar_companies(df, company_df,region_mapping,
                           vertical_filter,
                           industry_filter,
                           region_filter):
    
    df['Region Similarity'] = 0
    region_weight = 0
    
    model = SentenceTransformer('bert-base-uncased')

    company_df['value_proposition_embedding'] = company_df.apply(
        lambda x: model.encode(x['Company Value Proposition']),
        axis=1
    )

    df['value_proposition_embedding company'] = None
    df['value_proposition_embedding company'] = df['value_proposition_embedding company'].apply(lambda x: company_df.loc[0, 'value_proposition_embedding'])

    df['Company Similarity'] = df.apply(
        lambda x: util.pytorch_cos_sim(x['value_proposition_embedding'], x['value_proposition_embedding company'])[0][0].item(),
        axis=1
    )
    
    if(vertical_filter):
        print(company_df.loc[0, 'Company Vertical'])
        df = df[df['vertical']==company_df.loc[0, 'Company Vertical']].reset_index(drop=True)
    
    if(industry_filter):
        print(company_df.loc[0, 'Company Industry'])
        df = df[df['industry']==company_df.loc[0, 'Company Industry']].reset_index(drop=True)

    if(region_filter):
        print(region_mapping[company_df.loc[0, 'Company Headquarter']])
        df = df[df['exchange_symbol'].isin(region_mapping[company_df.loc[0, 'Company Headquarter']])].reset_index(drop=True)
    
    print(company_df.loc[0, 'Company Headquarter'])
    df['Final Similarity'] = (1-region_weight) * df['Company Similarity'] + region_weight * df['Region Similarity']
    
    competitor_df = df.sort_values(['Final Similarity'], ascending=False)[:15]
    competitor_df['Company Name'] = company_df.loc[0, 'Company Name']
    competitor_df['Company Headquarter'] = company_df.loc[0, 'Company Headquarter']
    competitor_df['Company Vertical'] = company_df.loc[0, 'Company Vertical']
    competitor_df['ticker'] = competitor_df['exchange_symbol'] + ": " + competitor_df['ticker']
    competitor_df = competitor_df[['Company Name', 'Company Headquarter', 'Company Vertical',
                                   'id', 'name', 'ticker', 'exchange', 'hq', 'value_proposition',
                                   'industry', 'vertical', 'target_audience', 'market', 'companytype',
                                   'companystatustype','Company Similarity', 'Region Similarity', 
                                   'Final Similarity']]
    competitor_df.rename(columns={'name': 'Competitor Name',
                                  'ticker': 'Competitor Ticker',
                                  'exchange': 'Competitor Exchange',
                                  'hq': 'Competitor Headquarter',
                                  'id': 'Competitor S&P Id',
                                  'value_proposition': 'Competitor Value Proposition',
                                  'industry': 'Competitor Industry',
                                  'vertical': 'Competitor Vertical',
                                  'target_audience': 'Competitor Audience',
                                  'market': 'Competitor Market',
                                  'companytype': 'Competitor Company Type',
                                  'companystatustype': 'Competitor Operating Status'},
                                  inplace=True)

    return competitor_df
