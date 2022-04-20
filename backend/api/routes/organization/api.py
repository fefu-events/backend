from fastapi import APIRouter

from backend.api.routes.organization import (
    organization,
    organization_member,
    organization_following,
    organization_transfer_owership
)


router = APIRouter()

router.include_router(organization.router,
                      tags=["organization"],
                      prefix="/organization")
router.include_router(organization_member.router,
                      tags=["organization member"],
                      prefix="/organization")
router.include_router(organization_following.router,
                      tags=["organization following"],
                      prefix="/organization")
router.include_router(organization_transfer_owership.router,
                      tags=["organization transfer ownership"],
                      prefix="/organization")
