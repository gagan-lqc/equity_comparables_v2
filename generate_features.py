# guidance.py
import re
import json

from guidance import models, gen, system, user, assistant, select


def get_company_features_guidance(model, comp_name: str, comp_ticker: str, comp_hq: str, 
                                  meta_title: str, meta_description: str, website_body: str) -> dict:
    with system():
        lm = model + "You are an experienced and helpful expert on company due-diligence processes. " \
            "The user will provide you with a details of a company, and you will return a complete VALID json list of value proposition,  industry, target_audience and market" \
            "To do this analysis well, you always use the following questions to help guide you in your step-by-step process:\n\n" \
            "1. What does the company try to achieve?\n" \
            "2. What products is it offering that will help it achieve its main goal?\n" \
            "3. Who does it target? B2C/B2B/B2E companies? millenials/aging population/kids? Large/SMB companies? etc.\n" \
            "4. Type of solution - is the company offering a marketplace? a platform to connect different players in the industry? Is it a physical product? etc.\n" \
            "5. Business model - SaaS/One-time payment? Does the company provide the product for free but get paid monthly for support? etc.\n" \
            "Use these questions to guide your analysis to come up with the best feature values that match on each of these questions.\n"


    with user():
        lm += f"""\
        The company name is : {comp_name} and their ticker symbol is : {comp_ticker} . /
        The company is headquartered in {comp_hq}./
        The meta title of their website : {meta_title} and meta description is {meta_description}.
        The body of their website contains : {website_body}

        In a JSON format:

        - Give me the value proposition of the company. In less than 100 words. In English. Casual Tone. Format is: "[Company Name] helps [target audience] [achieve desired outcome] and [additional benefit]"

        - Give me the industry of the company. (Classify using this industry list: [Agriculture, Arts, Construction, Consumer Goods, Education, Entertainment, Finance, Other, Health Care, Legal, Manufacturing, Media & Communications, Public Administration, Advertisements, Real Estate, Recreation & Travel, Retail, Software, Transportation & Logistics, Wellness & Fitness] if it's ambiguous between Sofware and Consumer Goods, prefer Consumer Goods)

        - Give me the vertical of the company. (classify using this vertical list: [SaaS, Ecommerce, FinTech, IndustrialTech, HealthTech, DeepTech, TMT, OTHER])
        
        - Guess the target audience of each company.(Classify and choose 1 from this list: [sales teams, marketing teams, HR teams, customer Service teams, consumers, C-levels] Write it in lowercase)

        - Tell me if they are B2B or B2C or B2E

        The output format should be as below.
        {{"value_proposition": value_proposition,
        "industry": industry,
        "vertical": vertical,
        "target_audience": target_audience, 
        "market": market }}
        """

    with assistant():
        try:
            lm += gen('answer', stop="]")
        except:
            lm += gen(regex="b''", name='answer')
    # Assuming JSON is single-line and starts with a curly brace '{'
    pattern = r"\s*\{(.*?)\}\s*"  
    match = re.search(pattern, lm['answer'], flags=re.DOTALL)

    if match:
        json_content = match.group(1)
        return json.loads('{'+json_content+'}')
    else:
        json_content = """
        {
            "value_proposition": "Not Found",
            "industry": "Not Found",
            "vertical": "Not Found",
            "market": "Not Found"
        }
        """
        print("No JSON found in the text")
        return json.loads(json_content)

