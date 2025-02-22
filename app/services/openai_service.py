from openai import OpenAI
from app.config import settings

client = OpenAI(api_key=settings.OPENAI_API_KEY)


def generate_visualization_code(dataset_info: str, prompt: str) -> str:
    combined_prompt = f"""You are a data visualization expert. Generate Python code using matplotlib/seaborn to create visualizations.
Requirements:
1. Use the DataFrame 'df' which is already loaded.
2. Create clear, well-labeled visualizations.
3. Include proper titles and labels.
4. Use appropriate color schemes.
5. Use only these libraries: 
pandas
matplotlib
seaborn
pydantic-settings
python-multipart
scikit-learn
statsmodels
prophet
6. Handle different data types appropriately.
Do not include plt.show() in the code.

Dataset info: {dataset_info}
User request: {prompt}
Only return the Python code, no explanations."""
    try:
        response = client.chat.completions.create(
            model="o1-mini-2024-09-12",  # Fixed model name
            messages=[{"role": "user", "content": combined_prompt}],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print(f"Error generating visualization code: {str(e)}")
        raise
