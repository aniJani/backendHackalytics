import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io
import base64


def analyze_dataset(file_path: str):
    file_extension = file_path.split(".")[-1].lower()

    if file_extension == "csv":
        df = pd.read_csv(file_path)
    elif file_extension in ["xlsx", "xls"]:
        df = pd.read_excel(file_path)
    elif file_extension == "json":
        df = pd.read_json(file_path)
    elif file_extension == "txt":
        # Assuming tab-separated values for txt files
        df = pd.read_csv(file_path, sep="\t")
    else:
        raise ValueError(f"Unsupported file type: {file_extension}")

    summary = {
        "columns": list(df.columns),
        "rows": len(df),
        "data_types": {str(k): str(v) for k, v in df.dtypes.items()},
        "sample": df.head(5).to_dict(),
    }
    return summary, df


def execute_visualization_code(code: str, dataset_path: str) -> str:
    try:
        # Clear any existing plots
        plt.clf()

        # Load the dataset
        df = pd.read_csv(dataset_path)

        # Create a new figure with a specific size
        plt.figure(figsize=(10, 6))
        print("Executing generated code:\n", code)
        if code.startswith("```"):
            code = "\n".join(code.split("\n")[1:-1])
        # Execute the visualization code with df, plt, and sns in the context
        exec(code, {"df": df, "plt": plt, "sns": sns})

        # Save the plot to a bytes buffer
        buffer = io.BytesIO()
        plt.savefig(buffer, format="png", bbox_inches="tight", dpi=300)
        buffer.seek(0)

        # Convert to base64
        image_base64 = base64.b64encode(buffer.getvalue()).decode()

        # Clean up
        plt.close("all")
        buffer.close()

        return image_base64
    except Exception as e:
        print(f"Error in execute_visualization_code: {str(e)}")
        raise
