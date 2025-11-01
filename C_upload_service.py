# upload_service.py
import os
import shutil
import pandas as pd
from fastapi import UploadFile, HTTPException

class UploadService:
    def __init__(self, upload_folder, app_state):
        self.UPLOAD_FOLDER = upload_folder
        self.app_state = app_state # Reference to the FastAPI app state

    async def handle_csv_upload(self, file: UploadFile) -> dict:
        """Saves the file and loads the data into app state."""
        file_location = os.path.join(self.UPLOAD_FOLDER, file.filename)
        
        try:
            # 1. Save file to disk
            with open(file_location, "wb") as buffer:
                # Note: file.file is a SpooledTemporaryFile or similar stream
                shutil.copyfileobj(file.file, buffer)
            
            # 2. Load data into app state
            # Assuming 'app_state' is where 'df' is stored (e.g., app.state)
            self.app_state.df = pd.read_csv(
                file_location, 
                index_col=0, 
                parse_dates=True
            )

            return {
                "filename": file.filename, 
                "detail": f"File successfully uploaded and saved to {file_location}"
            }
        except Exception as e:
            # Re-raise as HTTPException to be handled by FastAPI
            raise HTTPException(
                status_code=500, 
                detail=f"An error occurred during file upload or processing: {e}"
            )
        finally:
            await file.close()

# Note: You'll need to define UPLOAD_FOLDER and pass app_state from api.py