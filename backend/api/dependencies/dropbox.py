import dropbox

from backend.config import settings


def dropbox_connect():
    dbx = dropbox.Dropbox(**settings.dropbox_kwargs)
    return dbx
