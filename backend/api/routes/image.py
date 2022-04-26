from fastapi import APIRouter, Depends, UploadFile, File, Response
import dropbox

from backend import crud
from backend.schemas.user import UserInDBBase
from backend.api.dependencies.database import get_db
from backend.api.dependencies.user import get_current_user
from backend.api.dependencies.dropbox import dropbox_connect
import uuid

router = APIRouter()


@router.post(
    "/"
)
def write_image(
    image: UploadFile = File(...),
    dbx=Depends(dropbox_connect),
    db=Depends(get_db),
    user: UserInDBBase = Depends(get_current_user())
):
    generated_uuid = uuid.uuid4()
    dbx.files_upload(image.file.read(), f"/user-images/{generated_uuid}",
                     mode=dropbox.files.WriteMode("overwrite"))
    crud.user.set_image(db, user, generated_uuid)
    return generated_uuid


@router.get(
    "/{image_name}"
)
def get_image(
    image_name: str,
    dbx=Depends(dropbox_connect),
):
    _, result = dbx.files_download(path=f"/user-images/{image_name}")
    return Response(content=result.content, media_type="image/png")
