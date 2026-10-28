from fastapi import APIRouter,Depends,HTTPException,status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.dependencies import get_current_user
from app.models.job import job
from app.schema.job import jobCreate,jobResponse
from app.models.user import User

router=APIRouter(prefix="/jobs",tags=["jobs"])

@router.post("/",response_model=jobResponse,status_code=201)
def create_job(
    job_data:jobCreate,
    db:Session=Depends(get_db),
    current_user:User=Depends(get_current_user)
):
    new_job=job(company=job_data.company,
                role=job_data.role,
                location=job_data.location,
                job_type=job_data.job_type,
                salary=job_data.salary,
                description=job_data.description,
                job_url=job_data.job_url,
                user_id=current_user.id)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)
    return new_job