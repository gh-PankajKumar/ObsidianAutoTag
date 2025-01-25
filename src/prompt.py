from typing import Dict, List


def get_prompt(existing_tags: List[str]) -> Dict[str, str]:
    system_prompt = """
    You are a helpful assitant who is tasked with categorizing notes by assigning relevant tags that best describe their content. You will be provided with:

        A note to analyze.
        A list of existing tags to choose from."""

    prompt = f"""
    Instructions:

        Select one or more tags from the provided list that accurately categorize the note.
        Tags categorise the note based on its content and help users find related notes.
        Try to assign tags that are the most specific and relevant to the content of the note.
        Assign tags that are already in use given as the existing tags.
        If none of the existing tags are a match, you may create a new concise tag that best describes the content.
        Creating new tags should be done sparingly and only when necessary.
        Aim for clarity and relevance when assigning or creating tags.
        It is better to have less tags that are relevant than more tags that are irrelevant.
        Suggested tags should be enclosed in double square brackets, e.g., [[tag1]], [[tag2]].
        The output should be formatted: Suggested Tags: [[tag1]], [[tag2]]
        
    Example 1:
        Note: 
        # Fat Loss Made Simple
        ## Series of Lectures by Dr Mike Israetel

        ## Series Summary:

        First video discussed tracking current calorie to see where you are at and getting used to the idea of measuring food intake. The main points of the entire series are summarised below:
        **Macro nutrients:**
        - Aim for 1 g protein per lb of body weight
        - Aim for 0.5 g fat per lb of body weight 
        - Remaining calories from carbs

        **Meal timing and structure:**
        - 4 evenly spaced meals daily
        - Prioritise carbs around workouts, fats otherwise
        - Spread protein evenly

        - Stable water/salt intake helps track weight accurately
        - Current weight x desired weekly weight loss % x 500 calories = calorie deficit
        - Aim for 6-12 weeks of dieting
        - Increase activity to cover 50% of calorie reduction
        - Decrease fats for remaining deficit (min. 0.3 g/lb)
        - If weight loss stalls for 2 weeks, reduce intake by 250 calories
        Suggested Tags: [[Health & Fitness]]

    Example 2:
        # Overnight Oats 

        ## Macro Composition:
        - 400 calories
        - 37.5 g protein
        - 18.75 g fat
        -  21.5 g carbs
        ## Ingredients:
        - 40 g Oats
        - 150 ml Milk
        - 30 g Pea Protein
        - 10 g Hemp Protein

        ## Method:
        - Mix Oats and Milk to leave in fridge overnight
        - Mix in protein powders before eating
        Suggested Tags: [[Recipes]]

    Now, the existing tags are: {existing_tags}
    Categorize the following note:
    """
    return {"system_prompt": system_prompt, "prompt": prompt}
