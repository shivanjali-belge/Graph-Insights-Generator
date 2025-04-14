# from fastapi import FastAPI, File, UploadFile, HTTPException, Form
# import pandas as pd
# import io
# import os
# import base64
# import matplotlib.pyplot as plt
# import seaborn as sns
# from enum import Enum
# from google.generativeai import GenerativeModel, configure
# import uuid  # Import UUID for unique filenames
# from datetime import datetime
# from fastapi.staticfiles import StaticFiles


# app = FastAPI()
# UPLOAD_FOLDER = "static/uploads"
# GRAPH_FOLDER = "static/graphs"
# os.makedirs(UPLOAD_FOLDER, exist_ok=True)
# os.makedirs(GRAPH_FOLDER, exist_ok=True)
# app.mount("/static", StaticFiles(directory="static"), name="static")

# # Configure Gemini AI (Replace 'YOUR_GEMINI_API_KEY' with your actual key)
# configure(api_key="AIzaSyCxVoQcmKMJLhNRXc2rMDpyCtCJFeYVNmU")
# model = GenerativeModel("gemini-1.5-pro-latest")

# class GraphType(str, Enum):
#     bar = "bar"
#     line = "line"
#     scatter = "scatter"
#     heatmap = "heatmap"
#     pie = "pie"
#     histogram = "histogram"
#     boxplot = "boxplot"

# @app.post("/upload/")
# async def upload_file(file: UploadFile = File(...)):
#     try:
#         file_path = os.path.join(UPLOAD_FOLDER, file.filename)
#         with open(file_path, "wb") as f:
#             f.write(await file.read())
        
#         df = pd.read_csv(file_path)
#         columns = df.columns.tolist()
#         return {"message": "File uploaded successfully", "columns": columns, "file_path": file_path}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# @app.post("/generate_graph/")
# async def generate_graph(file_path: str = Form(...), graph_type: GraphType = Form(...), x_column: str = Form(...), y_column: str = Form(None)):
#     try:
#         df = pd.read_csv(file_path)
#         if x_column not in df.columns or y_column not in df.columns:
#             raise HTTPException(status_code=400, detail="Invalid column names")

#         plt.figure(figsize=(8, 6))
#         # if graph_type == GraphType.bar:
#         #     sns.barplot(x=df[x_column], y=df[y_column])
#         # elif graph_type == GraphType.line:
#         #     sns.lineplot(x=df[x_column], y=df[y_column])
#         # elif graph_type == GraphType.scatter:
#         #     sns.scatterplot(x=df[x_column], y=df[y_column])

#         if graph_type == GraphType.bar:
#             if y_column and pd.api.types.is_numeric_dtype(df[y_column]):
#                 sns.barplot(x=df[x_column], y=df[y_column])
#             else:
#                 sns.countplot(x=df[x_column])
#                 y_column = "count"

#         else:
#             if graph_type == GraphType.line:
#                 sns.lineplot(x=df[x_column], y=df[y_column])

#             elif graph_type == GraphType.scatter:
#                 sns.scatterplot(x=df[x_column], y=df[y_column])

#             elif graph_type == GraphType.heatmap:
#                 corr = df.corr(numeric_only=True)
#                 if corr.empty:
#                     raise HTTPException(status_code=400, detail="No numeric data available for heatmap.")
#                 sns.heatmap(corr, annot=True, cmap="coolwarm")
#                 x_column = "correlation_matrix"
#                 y_column = ""

#             elif graph_type == GraphType.pie:
#                 pie_data = df[x_column].value_counts()
#                 plt.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%', startangle=140)
#                 plt.axis('equal')
#                 y_column = "percentage"

#             elif graph_type == GraphType.histogram:
#                 sns.histplot(data=df, x=x_column, bins=10)

#             elif graph_type == GraphType.boxplot:
#                 sns.boxplot(x=df[x_column], y=df[y_column])


#         # Generate a unique filename using X & Y column names
#         safe_x_column = x_column.replace(" ", "_")  # Replace spaces with underscores
#         safe_y_column = y_column.replace(" ", "_")  # Replace spaces with underscores
#         unique_filename = f"{safe_x_column}_vs_{safe_y_column}_{uuid.uuid4().hex[:6]}.png"
#         graph_path = os.path.join(GRAPH_FOLDER, unique_filename)

#         plt.savefig(graph_path)
#         plt.close()
        
#         graph_url = f"http://127.0.0.1:8050/static/graphs/{unique_filename}"

#         return {"message": "Graph generated successfully", "graph_path": graph_path, "file_path": file_path,"graph_url":graph_url}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))

# # @app.post("/generate_insights/")
# # async def generate_insights(file_path: str = Form(...), user_query: str = Form(...)):
# #     try:
# #         df = pd.read_csv(file_path)
# #         data_sample = df.to_string()  
        
# #         prompt = f"Analyze the following dataset and answer the user's question.\n\nDataset:\n{data_sample}\n\nUser's Question: {user_query}"
# #         response = model.generate_content(prompt)
# #         insights = response.text if response else "Could not generate insights."
        
# #         return {"message": "Insights generated successfully", "insights": insights}
# #     except Exception as e:
# #         raise HTTPException(status_code=400, detail=str(e))

# # if __name__ == "__main__":
# #     import uvicorn
# #     uvicorn.run(app, host="127.0.0.1", port=8050)
# @app.post("/generate_insights/")
# async def generate_insights(file_path: str = Form(...), user_query: str = Form(...),graph_image: UploadFile = File(...)):
#     try:
        
#         df = pd.read_csv(file_path)
#         data_sample = df.to_string()  

#         # Identify the most recently generated graph
#         graph_files = sorted(os.listdir(GRAPH_FOLDER), key=lambda f: os.path.getctime(os.path.join(GRAPH_FOLDER, f)), reverse=True)
#         if not graph_files:
#             raise HTTPException(status_code=400, detail="No graphs found.")

#         latest_graph = graph_files[0]  # Get the most recent graph
#         graph_path = os.path.join(GRAPH_FOLDER, latest_graph)

#         # Extract graph details from filename (assuming format: "X_vs_Y_UUID.png")
#         graph_name_parts = latest_graph.split("_vs_")
#         x_column = graph_name_parts[0] if len(graph_name_parts) > 1 else "Unknown X"
#         y_column = graph_name_parts[1].split("_")[0] if len(graph_name_parts) > 1 else "Unknown Y"

#         # Construct an intelligent prompt for AI
#         prompt = f"""
#         You are analyzing a dataset that has been uploaded. Based on this dataset, a graph has been generated.
        
#         **Graph Details:**
#         - X-axis: {x_column}
#         - Y-axis: {y_column if y_column else "count (for bar chart without Y-axis)"}
        
#         **Dataset Preview:**
#         {data_sample}
        
#         **User Query:**
#         {user_query}
        
#         **Task:** 
#         Analyze the graph in the context of the uploaded dataset and provide meaningful insights. Identify trends, correlations, or key observations. Your response should be insightful and based on the dataset trends visible in the graph.
#         """

#         response = model.generate_content(prompt)
#         insights = response.text if response else "Could not generate insights."

#         return {"message": "Insights generated successfully", "insights": insights, "graph_path": graph_path}
#     except Exception as e:
#         raise HTTPException(status_code=400, detail=str(e))
    
# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8050)
from fastapi import FastAPI, File, UploadFile, HTTPException, Form
import pandas as pd
import os
import matplotlib.pyplot as plt
import seaborn as sns
from enum import Enum
from google.generativeai import GenerativeModel, configure
import uuid
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Configure folders
UPLOAD_FOLDER = "static/uploads"
GRAPH_FOLDER = "static/graphs"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(GRAPH_FOLDER, exist_ok=True)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configure Gemini AI
configure(api_key="AIzaSyCxVoQcmKMJLhNRXc2rMDpyCtCJFeYVNmU")
model = GenerativeModel("gemini-1.5-pro-latest")

class GraphType(str, Enum):
    bar = "bar"
    line = "line"
    scatter = "scatter"
    heatmap = "heatmap"
    pie = "pie"
    histogram = "histogram"
    boxplot = "boxplot"

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    try:
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())

        df = pd.read_csv(file_path)
        columns = df.columns.tolist()
        return {"message": "File uploaded successfully", "columns": columns, "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate_graph/")
async def generate_graph(file_path: str = Form(...), graph_type: GraphType = Form(...), x_column: str = Form(...), y_column: str = Form(None)):
    try:
        df = pd.read_csv(file_path)
        if x_column not in df.columns or (y_column and y_column not in df.columns):
            raise HTTPException(status_code=400, detail="Invalid column names")

        plt.figure(figsize=(8, 6))

        if graph_type == GraphType.bar:
            if y_column and pd.api.types.is_numeric_dtype(df[y_column]):
                sns.barplot(x=df[x_column], y=df[y_column])
            else:
                sns.countplot(x=df[x_column])
                y_column = "count"
        elif graph_type == GraphType.line:
            sns.lineplot(x=df[x_column], y=df[y_column])
        elif graph_type == GraphType.scatter:
            sns.scatterplot(x=df[x_column], y=df[y_column])
        elif graph_type == GraphType.heatmap:
            corr = df.corr(numeric_only=True)
            if corr.empty:
                raise HTTPException(status_code=400, detail="No numeric data available for heatmap.")
            sns.heatmap(corr, annot=True, cmap="coolwarm")
            x_column = "correlation_matrix"
            y_column = ""
        elif graph_type == GraphType.pie:
            pie_data = df[x_column].value_counts()
            plt.pie(pie_data.values, labels=pie_data.index, autopct='%1.1f%%', startangle=140)
            plt.axis('equal')
            y_column = "percentage"
        elif graph_type == GraphType.histogram:
            sns.histplot(data=df, x=x_column, bins=10)
        elif graph_type == GraphType.boxplot:
            sns.boxplot(x=df[x_column], y=df[y_column])

        safe_x_column = x_column.replace(" ", "_")
        safe_y_column = y_column.replace(" ", "_") if y_column else "none"
        unique_filename = f"{safe_x_column}vs{safe_y_column}_{uuid.uuid4().hex[:6]}.png"
        graph_path = os.path.join(GRAPH_FOLDER, unique_filename)

        plt.savefig(graph_path)
        plt.close()

        graph_url = f"http://127.0.0.1:8050/static/graphs/{unique_filename}"

        return {
            "message": "Graph generated successfully",
            "graph_path": graph_path,
            "file_path": file_path,
            "graph_url": graph_url
        }
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/generate_insights/")
async def generate_insights(
    file_path: str = Form(...),
    user_query: str = Form("auto")
):
    try:
        # Load dataset
        df = pd.read_csv(file_path)
        data_sample = df.head(10).to_string()

        # Get latest graph file
        graph_files = sorted(
            [f for f in os.listdir(GRAPH_FOLDER) if f.endswith(".png")],
            key=lambda f: os.path.getctime(os.path.join(GRAPH_FOLDER, f)),
            reverse=True
        )
        
        if not graph_files:
            raise HTTPException(status_code=400, detail="No graph images found. Please generate a graph first.")

        latest_graph_file = graph_files[0]
        graph_path = os.path.join(GRAPH_FOLDER, latest_graph_file)

        # Read graph image as binary (no base64 conversion needed)
        with open(graph_path, "rb") as image_file:
            image_bytes = image_file.read()

        # Extract graph info from filename
        filename_parts = latest_graph_file.replace(".png", "").split("vs")
        x_column = filename_parts[0]
        y_column = filename_parts[1] if len(filename_parts) > 1 else None

        # Detect graph type from filename
        graph_type = "unknown"
        for gtype in GraphType:
            if gtype.value in latest_graph_file.lower():
                graph_type = gtype.value
                break

        # Prepare the prompt
        if user_query.strip().lower() == "auto":
            prompt = f"""
            Analyze this {graph_type} graph showing {x_column} vs {y_column if y_column else 'count'}.
            Provide:
            1. Key insights from the visualization
            2. 2-3 interesting questions we could explore next
            3. Any data quality issues or anomalies you notice
            
            Dataset sample:
            {data_sample}
            """
        else:
            prompt = f"""
            Regarding this {graph_type} graph showing {x_column} vs {y_column if y_column else 'count'}:
            {user_query}
            
            Dataset sample:
            {data_sample}
            """

        # Call Gemini with binary image data directly
        response = model.generate_content(
            contents=[
                {"text": prompt},
                {"mime_type": "image/png", "data": image_bytes}
            ]
        )
        
        if not response or not response.text:
            raise HTTPException(status_code=400, detail="Empty response from Gemini API")

        insights = response.text

        return {
            "message": "Insights generated successfully",
            "insights": insights,
            "graph_url": f"/static/graphs/{latest_graph_file}",
            "graph_type": graph_type,
            "x_column": x_column,
            "y_column": y_column
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8050)